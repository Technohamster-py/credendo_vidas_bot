import settings
import readqr as qr
import database as db
import os
import time
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


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    take_btn = types.KeyboardButton(config.get('Buttons', 'take'))
    put_btn = types.KeyboardButton(config.get('Buttons', 'put'))
    markup.add(take_btn, put_btn)
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    hello_message = config.get('Messages', 'hello')
    bot.send_message(message.chat.id, hello_message)
    if not check_username(message.chat.username):
        username_err_message = config.get('Messages', 'username_err')
        bot.send_message(message.chat.id, username_err_message)
    else:
        username_succ_message = config.get('Messages', 'username_succ')
        bot.send_message(message.chat.id, username_succ_message, reply_markup=main_menu())


@bot.message_handler(commands=['checkme'])
def check_user(message):
    if not check_username(message.chat.username):
        username_err_message = config.get('Messages', 'username_err')
        bot.send_message(message.chat.id, username_err_message, reply_markup=types.ReplyKeyboardRemove())
    else:
        username_succ_message = config.get('Messages', 'username_succ')
        bot.send_message(message.chat.id, username_succ_message, reply_markup=main_menu())


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == config.get('Buttons', 'take'):
        qr_request_message = config.get('Messages', 'take_req')
        send = bot.send_message(message.chat.id, qr_request_message, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, take)
    elif message.text == config.get('Buttons', 'take'):
        qr_request_message = config.get('Messages', 'take_req')
        send = bot.send_message(message.chat.id, qr_request_message, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, put)
    else:
        err_message = config.get('Messages', 'command_err')
        bot.send_message(message.chat.id, err_message)


@bot.message_handler(content_types=['photo'])
def take(message):
    raw_photo = message.photo[-1].file_id
    filename = 'tmp/' + raw_photo + '.jpg'
    file_info = bot.get_file(raw_photo)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    data = qr.read_qr(filename)
    os.remove(filename)

    bot.send_message(message.chat.id, config.get('Messages', 'operation_succ'), reply_markup=main_menu())


@bot.message_handler(content_types=['photo'])
def put(message):
    pass


if __name__ == '__main__':
    bot.infinity_polling()