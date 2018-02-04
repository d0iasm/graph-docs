#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


API_TOKEN = os.environ['SLACKBOT_API_TOKEN']

PLUGINS = [
    'slackbot.plugins',
    'plugins'
    ]

DEFAULT_REPLY = "You can ask me for help by `@graphy help` or `@graphy ヘルプ`"
