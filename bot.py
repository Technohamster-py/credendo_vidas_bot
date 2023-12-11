import settings
import qr_functions as qr
import os
import telebot
from telebot import types
from item import Item
from user import User

config = settings.load_config()
private_config = settings.load_config('private_settings.ini')
TOKEN = private_config.get('Settings', 'token')

bot = telebot.TeleBot(TOKEN)


def check_username(username):
    with open('whitelist.txt', mode='r') as rf:
        usernames = [line for line in rf]
    return username in usernames


def get_main_menu():
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
        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_err'))
    else:
        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_succ'),
                         reply_markup=get_main_menu())


@bot.message_handler(commands=['checkme'])
def check_user(message):
    if not check_username(message.chat.username):
        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_err'),
                         reply_markup=types.ReplyKeyboardRemove())
    else:

        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_succ'),
                         reply_markup=get_main_menu())


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == config.get('Buttons', 'take'):
        send = bot.send_message(message.chat.id,
                                config.get('Messages', 'take_req'),
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, take)

    elif message.text == config.get('Buttons', 'put'):
        send = bot.send_message(message.chat.id,
                                config.get('Messages', 'put_req'),
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, put)

    else:
        bot.send_message(message.chat.id,
                         config.get('Messages', 'command_err'))


@bot.message_handler(content_types=['photo'])
def take(message):
    if check_username(message.chat.username):
        raw_photo = message.photo[-1].file_id
        filename = 'tmp/' + raw_photo + '.jpg'
        file_info = bot.get_file(raw_photo)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        data = qr.read_qr(private_config.get('Settings', 'rgx'), filename)
        os.remove(filename)

        user = User(message.chat.username, private_config.get('Settings', 'db_path'))
        if user.user_id:
            item = Item(data, private_config.get('Settings', 'db_path'))
            status = item.take(user.last_name, user.first_name)
            if status:
                if status != -1:
                    bot.send_message(message.chat.id,
                                     config.get('Messages', 'operation_succ'),
                                     reply_markup=get_main_menu())
                else:
                    bot.send_message(message.chat.id,
                                     config.get('Messages', 'quantity_err'),
                                     reply_markup=get_main_menu())
            else:
                bot.send_message(message.chat.id,
                                 config.get('Messages', 'operation_err'),
                                 reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_err'),
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['photo'])
def put(message):
    if check_username(message.chat.username):
        raw_photo = message.photo[-1].file_id
        filename = 'tmp/' + raw_photo + '.jpg'
        file_info = bot.get_file(raw_photo)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        data = qr.read_qr(private_config.get('Settings', 'rgx'), filename)
        os.remove(filename)
        if data:
            user = User(message.chat.username, private_config.get('Settings', 'db_path'))
            if user.user_id:
                item = Item(data, private_config.get('Settings', 'db_path'))
                status = item.put(user.last_name, user.first_name)
                if status:
                    if status != -1:
                        bot.send_message(message.chat.id,
                                         config.get('Messages', 'operation_succ'),
                                         reply_markup=get_main_menu())
                    else:
                        bot.send_message(message.chat.id,
                                         config.get('Messages', 'overload_err'),
                                         reply_markup=get_main_menu())
                else:
                    bot.send_message(message.chat.id,
                                     config.get('Messages', 'operation_err'),
                                     reply_markup=get_main_menu())
        else:
            bot.send_message(message.chat.id,
                             config.get('Messages', 'qr_err'),
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         config.get('Messages', 'username_err'),
                         reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.infinity_polling()