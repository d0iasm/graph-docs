import boto3
import datetime
import graphviz
import os

# from . import parser
import parser
# from . import weighting
import weighting


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self, new_text):
        print('debug renderer init')
        self.dot = graphviz.Graph(format='png', engine='neato',
                                  edge_attr={'color': 'white', 'fontsize': '14', 'len': '2'},
                                  graph_attr={'overlap': 'false', 'bgcolor': '#343434',
                                              'fontcolor': 'white', 'style': 'filled',},
                                  node_attr={'fixedsize': 'true', 'style': 'solid,filled',
                                             'color': 'black', 'shape': 'circle', 'colorscheme': 'gnbu7',
                                             'fontcolor': 'black', 'fontsize': '16'})
        self.parser = parser.Parser()
        self.new = new_text
        # TODO: Bucket policy
        self.session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                             aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                             region_name='ap-northeast-1')
        self.s3 = self.session.resource('s3')
        self.s3_bucket = os.environ['S3_BUCKET_NAME']

        
    def add_edges(self):
        """
        :param string line: a natural language text for parsing.
        """
        for child, parent in self.parser.find_parent_child():
            self.dot.edge(child, parent)
            
        
    def add_nodes(self):
        nodes = self.parser.find_nodes()
        edges = self.parser.find_parent_child()
        w_nodes = weighting.weighting(nodes, edges)
        for node in w_nodes:
            self.dot.node(node[0], label=node[0], **node[1])

            
    def copy(self):
        self.s3.Object(self.s3_bucket, 'old').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'new'})

        
    def render(self, text):
        self.parser.set(text)
        self.add_nodes()
        self.add_edges()
        name = 'results/result_' + datetime.datetime.now().strftime('%s') + '.png'
        print("[Debug] dot file content: " + self.dot.source)
        self.s3.Object(self.s3_bucket, name).put(
            Body=graphviz.Source(self.dot.source, engine='neato', encoding='utf-8', format='png').pipe())
        return name, text

    
    def reset(self):
        self.s3.Object(self.s3_bucket, 'old').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'empty'})
        self.s3.Object(self.s3_bucket, 'new').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'empty'})

        
    def merge(self):
        old_text = self.s3.Object(
            self.s3_bucket, 'old').get()['Body'].read().decode('utf-8')

        return (old_text + self.new).strip()

    
    def save(self, text):
        self.s3.Object(self.s3_bucket, 'new').put(Body=text)

        
    def debug(self, text):
        self.parser.set(text)
        self.add_nodes()
        self.add_edges()
        print(self.dot.source)
        self.dot.render('debug', view=True, cleanup=True)


if __name__ == '__main__':
    line = """テストメッセージ。"""
    print(len(line))
    r = Renderer(line)
    r.debug(line)
