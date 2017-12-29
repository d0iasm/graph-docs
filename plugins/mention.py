import json
import re
from slackbot.bot import listen_to
from slackbot.bot import respond_to


from . import renderer


count = 0
text = ''


@respond_to('(リセット|reset)', re.IGNORECASE)
def reset_image(message, content):
    r = renderer.Renderer('')
    r.reset()
    message.reply('DONE: Reset the past text.')


@listen_to('(.*)')
def create_image(message, content):
    global count, text
    count += 1
    text += content
    if count >= 1:
        file_name, all_text = render(text)
        attachments = [{
            'text': all_text,
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
