#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import requests
from slackbot.bot import listen_to
from slackbot.bot import respond_to


from . import renderer


text = ''
text_data = []
# text_data = [
        # {
            # 'text': <text content>,
            # 'channel': <channel ID>,
            # 'message_ts': <thread_ts>,
        # },
        # {
            # 'message': ...,
        # }
    # ]


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
    global text, text_data
    text = ''
    text_data = []
    message.reply('DONE: Reset the past text')
    print('Debug: Reset the past text')


@listen_to('(.*)', re.DOTALL)
def create_image(message, content):
    global text, text_data
    text += content
    text_data.append({
        'text': content,
        'channel': message.body['channel'],
        'message_ts': message.thread_ts,
        'permalink': get_permalink(message.body['channel'], message.thread_ts),
        })

    print('Debug: Current text length ', len(text))
    print('Debug: Current text ', text)
    print('Debug: Current test data', text_data)

    if len(text) > 70:
        r = renderer.Renderer(text)
        file_name = r.render(text)
        attachments = [{
            'text': "\n".join([d['text'] + ': ' + d['permalink'] for d in text_data]),
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/' + file_name,
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))


def get_permalink(channel, thread_ts):
    headers = {
        'Accept': 'application/x-www-form-urlencoded',
    }

    params = (
        ('token', os.environ['SLACKBOT_API_TOKEN']),
        ('channel', channel),
        ('message_ts', thread_ts),
    )

    response = requests.get('https://slack.com/api/chat.getPermalink', headers=headers, params=params)

    if response.status_code == 200:
        print('debug: print response', response.json()['permalink'])
        return response.json()['permalink']
    else:
        print('ERROR: failed to request')
        return None
