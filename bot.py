import settings
#import qrcode as qr
import telebot
from telebot import types


config = settings.load_config()
TOKEN = config.get('Settings', 'token')

bot = telebot.TeleBot(TOKEN)


def check_username(username):
    with open('whitelist.txt', mode='r') as rf:
        usernames = [line for line in rf]
    return username in usernames


@bot.message_handler(commands=['start'])
def start_message(message):
    hello_message = config.get('Messages', 'hello')
    bot.send_message(message.chat.id, hello_message)
    if not check_username(message.chat.username):
        username_err_message = config.get('Messages', 'username_err')
        bot.send_message(message.chat.id, username_err_message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        take_btn = types.KeyboardButton(config.get('Buttons', 'take'))
        put_btn = types.KeyboardButton(config.get('Buttons', 'put'))
        markup.add(take_btn, put_btn)
        username_succ_message = config.get('Messages', 'username_succ')
        bot.send_message(message.chat.id, username_succ_message, reply_markup=markup)


@bot.message_handler(commands=['checkme'])
def check_user(message):

bot.infinity_polling()