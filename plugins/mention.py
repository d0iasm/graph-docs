from slackbot.bot import listen_to


count = 0
text = ''


@listen_to('(.*)')
def listen_func(message, content):
    global count, text
    count += 1
    text += content
    if count >= 2:
        message.reply('Create a graph from the following text \n```' + text + '```')
        count = 0
        text = ''
