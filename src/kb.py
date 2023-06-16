from telegram import InlineKeyboardButton
from messages import *
reply_keyboard_first_menu = [["Калькулятор сна", "Статьи", "Промокод"]]

KEYBOARD_OF_ARTICLES = [[InlineKeyboardButton(f"{key}", callback_data=f"{value}", url=value)] for key, value in ARTICLES.items()]