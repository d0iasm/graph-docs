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
    r = renderer.Renderer('')
    r.reset()
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
        })
    print('Debug: Current text length ', len(text))
    print('Debug: Current text ', text)
    print('Debug: Current test data', text_data)
    if len(text) > 70:
        print('[Debug] start to render')
        file_name, all_text = render(text)
        print('[Debug] end to render and get file name', file_name)
        attachments = [{
            'text': ' ',
            'image_url': 'https://s3-ap-northeast-1.amazonaws.com/graphy-bot/' + file_name,
        }]
        message.send_webapi(' ', attachments=json.dumps(attachments))
        text = ''
        text_data = []


@respond_to('hoge', re.IGNORECASE)
def hoge(message):
    print('debug: thread_ts is ', message.thread_ts)
    print('debug: channel is ', message.body['channel'])
    print('debug: token is ', os.environ['SLACKBOT_API_TOKEN'])
    print('debug: channel object is ', message.channel)
    print('debug: message body is ', message.body)
    get_permalink(message.body['channel'], message.thread_ts)


def render(text):
    r = renderer.Renderer(text)
    r.copy()
    merged_text = r.merge()
    r.save(merged_text)
    return r.render(merged_text)


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
        print('debug: print response', response.json())
    else:
        print('ERROR: failed to request')
