import logging, datetime, config
from messages import *
from kb import *

from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update, 
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Настройка журналирования
logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = HELLO_MESSAGE,
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_first_menu,
         resize_keyboard=True,
         one_time_keyboard=True),
   )
   # Логи выбора из начального меню - кнопок
   user = update.message.from_user
   logger.info("Choice of %s: %s", user.first_name, update.message.text)

   return CHOICE

# Получаем от пользователя время предположительного подъема
async def getting_up_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=GETTING_UP_TIME_TEXT
   )
   return TIME_OF_WAKEUP

# Получаем от пользователя количество часов сна
async def getting_amountHours(update: Update, context: ContextTypes.DEFAULT_TYPE):
   string_fromUsers = update.message.text
   global wake_up_hour, wake_up_minute

   try:
      wake_up_hour, wake_up_minute = map(int, string_fromUsers.split(":"))
      
   except:
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text=ERROR_TEXT_OF_TIME
      )
      return CHOICE
   
   await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text=GETTING_HOURS_OF_SLEEP_TEXT
      )
   return HOURS

# Обрабатываем полученные данные и выдаем результат пользователю
async def calculate_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        amount_hours = int(update.message.text)
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ERROR_TEXT_AMOUNT_OF_HOURS
        )
        return TIME_OF_WAKEUP
   
    current_time = datetime.datetime.now()

    # Преобразуем введенное время для пробуждения в объект времени
    wake_up = current_time.replace(hour=wake_up_hour, minute=wake_up_minute, second=0, microsecond=0)

    # Если введенное время для пробуждения уже прошло сегодня, добавляем 1 день
    if wake_up < current_time:
        wake_up += datetime.timedelta(days=1)
    
    # Вычисляем оптимальное время для засыпания, вычитая выбранное кол-во сна от пользователя
    bedtime = wake_up - datetime.timedelta(hours=amount_hours)

    while bedtime < current_time:
        bedtime += datetime.timedelta(hours=1, minutes=30)
   
    bedtime = str(bedtime.strftime("%H:%M"))
    print(bedtime)

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text=f"{TIME_OF_WAKEUP}: {bedtime}", 
    )
    # Возврат пользователя в главное меню
    return CHOICE

# Выбор пользователем статьи из списка
async def article_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

   reply_markup = InlineKeyboardMarkup(inline_keyboard=KEYBOARD_OF_ARTICLES)

   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=TEXT_LIST_OF_ARTICLES,
      reply_markup=reply_markup
   )
   #return BUTTON - возможно пригодится

# Завершение диалога с ботом
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await context.bot.send_message(
       chat_id= update.effective_chat.id,
       text= BYE_TEXT, reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END