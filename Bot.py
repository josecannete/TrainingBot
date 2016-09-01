from telegram.ext import Updater
from codeforces import CodeforcesAPI
import logging
from telegram.ext import CommandHandler
from utils import unsolved_group
from utils import random_problem
import random

updater = Updater(token='262573736:AAEfHFSGp-5YGJFIiDt8_TmSZMR0XCHjtTg')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


api = CodeforcesAPI()

# DEFINITIONS OF FUNCTIONS

def error(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")

def hello(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hello {}'.format(update.message.from_user.first_name))

def rate_change(bot, update, args):
    if len(args) <= 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="wat is dis")
        return
    text = 'El rating change de ' + args[0] + ' es  \n'
    rating_changes = list(api.user_rating(args[0]))
    for rating in rating_changes:
        text += str(rating.old_rating)
        text += ' -> '
    text += str(rating_changes[-1].new_rating)
    bot.sendMessage(update.message.chat_id, text = text)


def contest_hacks(bot, update, args):
    return

def handle_info(bot, update, args):
    if len(args) <= 0:
        error(bot, update)
        return
    handles = []
    message = ''
    for handle in args:
        handles.append(handle)
    info = api.user_info(handles)
    for handle in info:
        message += ('Handle: ' + str(handle.handle) + '\n' )
        message += ('Rank: ' + str(handle.rank) + '\n' )
        message += ('Rating: ' + str(handle.rating) + '\n')
        message += '\n'
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def last_submissions(bot, update, args):
    if len(args) != 2:
        error(bot, update)
        return
    message = ''
    count = int(args[0])
    handle = args[1]
    submissions = api.user_status(handle, 1, count)
    for sub in submissions:
        message += str(sub.problem.name) + ' ---------> ' + str(sub.verdict.value) + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def random_unsolved(bot, update, args):
    if len(args) != 1:
        error(bot, update)
        return
    unsolved = unsolved_group(args[0])
    problem = random.choice(unsolved)
    message = str(problem.contest_id) + str(problem.index) + ' ' + str(problem.name) + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def randomp(bot, update, args):
    if len(args) > 3:
        error(bot, update)
        return
    string = ''
    for word in args:
        string += word + ' '
    print(string)
    string = string[0:len(string)-1]
    print(string)
    problem = random_problem(str(string))
    if (problem == False):
        error(bot, update)
        return
    message = str(problem.contest_id) + str(problem.index) + ' ' + str(problem.name) + '\n'
    bot.sendMessage(chat_id=update.message.chat_id, text=message)






# CREATE HANDLERS AND DISPATCHERS
random_unsolved_handler = CommandHandler('random_unsolved', random_unsolved , pass_args = True)
last_submissions_handler = CommandHandler('last_submissions', last_submissions , pass_args = True)
rate_change_handler = CommandHandler('rate_change', rate_change, pass_args = True)
handle_info_handler = CommandHandler('handle_info', handle_info, pass_args = True)
randomp_handler = CommandHandler('randomp', randomp, pass_args = True)
start_handler = CommandHandler('start', start)
hello_handler = CommandHandler('hello',hello)

dispatcher.add_handler(random_unsolved_handler)
dispatcher.add_handler(last_submissions_handler)
dispatcher.add_handler(handle_info_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(rate_change_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(randomp_handler)

updater.start_polling()
updater.idle()