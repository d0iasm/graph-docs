import json
import re
from slackbot.bot import listen_to
from slackbot.bot import respond_to


from . import renderer


text = ''


@respond_to('ヘルプ|help', re.IGNORECASE)
def help(message):
    message.reply("""
You can ask me one of the following questions by mentioning such as `@graphy`:
`リセット` or `reset`: You can delete all past text to initialize an image.
`ヘルプ` or `help`: You can know how to use this bot. this message will be sent.

This bot listen all text and create an image from it automatically if you invite this bot and do not mention.You can remove this bot whenever you want to.
""")

    
@respond_to('リセット|reset', re.IGNORECASE)
def reset_image(message):
    global text
    text = ''
    r = renderer.Renderer('')
    r.reset()
    message.reply('DONE: Reset the past text.')


@listen_to('(.*)')
def create_image(message, content):
    global text
    text += content
    print("[Debug] Current text length: " + str(len(text)))
    print("[Debug] Current text: " + text)
    if len(text) > 300:
        file_name, all_text = render(text)
        attachments = [{
            'text': ' ',
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/' + file_name,
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))
        text = ''


def render(text):
    r = renderer.Renderer(text)
    r.copy()
    merged_text = r.merge()
    r.save(merged_text)
    return r.render(merged_text)
