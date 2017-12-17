import json
from slackbot.bot import listen_to
from slackbot.bot import respond_to

from . import renderer


count = 0
text = ''


import sys
import logging
import os
@respond_to('hoge')
def hoge(message):
    logging.error(os.path)
    logging.error(sys.getcwd())
    attachments = [{
        'text': 'fuga',
        'image_url': 'https://placehold.jp/150x150.png',
    }]
    message.send_webapi('hoge', attachments=json.dumps(attachments))


@listen_to('(.*)')
def listen_func(message, content):
    global count, text
    render(text)
    count += 1
    text += content
    if count >= 2:
        # message.reply('Create a graph from the following text \n```' + text + '```')
        attachments = [{
            'text': 'Create a graph from the following text\n' + text,
            'image_url': '/app/dest/result.png',
        }]
        message.send_webapi('hoge', attachments=json.dumps(attachments))
        count = 0
        text = ''


def render(text):
    old = '/app/dest/old.dot'
    new = '/app/dest/new.dot'
    merge = '/app/dest/merge.dot'
    result = '/app/dest/result'
    r = renderer.Renderer()
    r.copy(merge, old)
    r.add_nodes(text)
    r.add_edges(text)
    r.save(new)
    r.merge(old, new, merge)
    r.render_from_dot(merge, result)
