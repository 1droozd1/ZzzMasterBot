from telegram import InlineKeyboardButton
from messages import *
import emoji

start_key = [InlineKeyboardButton("Давай начнем!", callback_data="Давай начнем!")]
reply_keyboard_first_menu = [["Калькулятор сна", "Статьи", "Промокод", emoji.emojize("Пока:waving_hand:")]]

KEYBOARD_OF_ARTICLES = [InlineKeyboardButton(f"{key}", callback_data=f"{value}", url=value) for key, value in ARTICLES.items()]
BACK_KEY = [InlineKeyboardButton("Назад в меню", callback_data="Назад в меню")]
BYE_KEY = [InlineKeyboardButton(emoji.emojize("Пока:waving_hand:"), callback_data="Пока")]

END_OF_FUNCTION_KEYBOARD = [["Назад в меню", "Пока!"]]