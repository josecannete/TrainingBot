from telegram.ext import Updater
from codeforces import CodeforcesAPI

updater = Updater(token='262573736:AAEfHFSGp-5YGJFIiDt8_TmSZMR0XCHjtTg')

dispatcher = updater.dispatcher

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")

def hello(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hello {}'.format(update.message.from_user.first_name))

api = CodeforcesAPI()

handle = 'Choreza'

rating_changes = list(api.user_rating(handle))
print('Rating history for {}:'.format(handle))
for rating in rating_changes:
     print(rating.old_rating, end=' -> ')

print(rating_changes[-1].new_rating)

def handle(bot, update, args):
    if (len(args) <= 0):
        bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")
        return
    text = 'El rating change de ' + args[0] + ' es  \n'
    rating_changes = list(api.user_rating(args[0]))
    for rating in rating_changes:
        text += str(rating.old_rating)
        text += ' -> '
    text += str(rating_changes[-1].new_rating)
    bot.sendMessage(update.message.chat_id, text = text)

from telegram.ext import CommandHandler

handle_handler = CommandHandler('handle', handle, pass_args = True)
start_handler = CommandHandler('start', start)
hello_handler = CommandHandler('hello',hello)

dispatcher.add_handler(hello_handler)
dispatcher.add_handler(handle_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()