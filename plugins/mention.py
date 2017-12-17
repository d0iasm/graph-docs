from slackbot.bot import listen_to
import json

from . import renderer


count = 0
text = ''


@listen_to('(.*)')
def listen_func(message, content):
    global count, text
    render(text)
    count += 1
    text += content
    message.reply('Hello')
    if count >= 2:
        # message.reply('Create a graph from the following text \n```' + text + '```')
        attachments = [{
            'text': 'Create a graph from the following text \n```' + text + '```',
            'image_url': './dest/result.png',
        }]
        message.send_webapi('', json.dumps(attachments))
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
