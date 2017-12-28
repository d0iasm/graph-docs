import json
from slackbot.bot import listen_to

from . import renderer


count = 0
text = ''


@listen_to('(.*)')
def listen_func(message, content):
    global count, text
    render(text)
    count += 1
    text += content
    if count >= 1:
        attachments = [{
            'text': text,
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/result.png',
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))
        count = 0
        text = ''


def render(text):
    old = './dest/old.dot'
    new = './dest/new.dot'
    merge = './dest/merge.dot'
    result = './dest/result'
    r = renderer.Renderer()
    r.copy(merge, old)
    r.add_nodes(text)
    r.add_edges(text)
    r.save(new)
    r.merge(old, new, merge)
    r.render_from_dot(merge, result)
