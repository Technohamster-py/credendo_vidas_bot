import settings
import qrcode as qr
import telebot


config = settings.load_config()
TOKEN = config.get('Settings', 'token')

bot = telebot.TeleBot(TOKEN)
