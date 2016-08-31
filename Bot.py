from telegram.ext import Updater

updater = Updater(token='262573736:AAEfHFSGp-5YGJFIiDt8_TmSZMR0XCHjtTg')

dispatcher = updater.dispatcher

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")

def hello(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hello {}'.format(update.message.from_user.first_name))


from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
hello_handler = CommandHandler('hello',hello)

dispatcher.add_handler(hello_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()