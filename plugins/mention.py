import json
import time
from slackbot.bot import listen_to

from . import renderer


count = 0
text = ''


@listen_to('(.*)')
def listen_func(message, content):
    global count, text
    count += 1
    text += content
    if count >= 1:
        file_name = render(text)
        attachments = [{
            'text': text,
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/' + file_name,
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))
        count = 0
        text = ''


def render(text):
    r = renderer.Renderer(text)
    r.copy()
    merged_text = r.merge()
    r.save(merged_text)
    return r.render(merged_text)
