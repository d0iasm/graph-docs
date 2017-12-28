import json
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
        render(text)
        attachments = [{
            'text': text,
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/result.png',
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))
        count = 0
        text = ''


def render(text):
    r = renderer.Renderer(text)
    merged_text = r.merge()
    r.save(merged_text)
    r.render(merged_text)
