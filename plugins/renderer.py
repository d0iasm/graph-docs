import boto3
import datetime
import graphviz
import os

from . import parser
# import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self, new_text):
        self.dot = graphviz.Graph(format='png', engine='neato',
                                  edge_attr={'color': 'white', 'fontsize': '14', 'len': '2'},
                                  graph_attr={'overlap': 'false', 'bgcolor': '#343434',
                                              'fontcolor': 'white', 'style': 'filled',},
                                  node_attr={'fixedsize': 'true', 'style': 'solid,filled',
                                             'color': 'black', 'shape': 'circle', 'colorscheme': 'gnbu5',
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
        """
        :param string line: a natural language text for parsing.
        """
        for node in self.parser.find_nodes():
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
            Body=graphviz.Source(self.dot.source, engine='neato', format='png').pipe())
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
    line = """この冬一番の強い寒気の影響で、西日本から北日本にかけての広い範囲で雪が降り、新潟県の山間部ではこの24時間に降った雪の量が70センチを超えている。この強い雪は12日にかけても続く見通しで、12日の予想降雪量は北陸地方（石川県を中心に）で70センチ、北海道と近畿地方で50センチなど広い範囲で大雪に警戒が必要だ。
今季最強寒気　12日も日本海側で大雪続く。九州や四国でも積雪　12日にかけても日本海側中心に大雪のおそれ
　11日は九州や四国でも今シーズン初めて本格的な雪が降り、長崎県長崎市や熊本県熊本市でも雪が積もった。また、四国山地では大雪となっていて、愛媛県久万高原町では午後3時の積雪が36センチに達した。"""
    print(len(line))
    r = Renderer(line)
    r.debug(line)
