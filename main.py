import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import datetime

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Настройка журналирования
logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOICE = 0

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   reply_keyboard = [["Калькулятор сна", "Статьи", "Промокод"]]

   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = """Привет! Я могу помочь тебе определить оптимальное время для засыпания и пробуждения. Выбери один из предложенных вариантов моих функций.""",
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard, 
         one_time_keyboard=True),
   )
   return CHOICE

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   user = update.message.from_user
   logger.info("Choice of %s: %s", user.first_name, update.message.text)

   if update.message.text == "Калькулятор сна":
      CHOICE = 0
   elif update.message.text == "Статьи":
      CHOICE = 1
   else:
      CHOICE = 2

   await context.bot.send_message(
      chat_id= update.effective_chat.id,
      text=f"Выбранная вами команда: {update.message.text}"
   )

   return CHOICE

async def getting_time_fromUsers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Укажите желаемое время пробуждения в формате ЧЧ:ММ"
   )

   string_fromUsers = update.message.text

   try:
      wake_up_hour, wake_up_minute = map(int, string_fromUsers.split(":"))
      
   except:
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Извините, произошла ошибка. Пожалуйста, укажите время проснуться в формате ЧЧ:ММ."
      )
   
   await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text="Отлично! Теперь укажите длительность сна, которую вы предпочитаете (в часах)."
      )
   
   try:
      amount_hours = int(update.message.text)
   except:
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Извините, произошла ошибка. Пожалуйста, укажите длительность сна, которую вы предпочитаете (в часах)."
      )
   
   current_time = datetime.datetime.now()

   # Преобразуем введенное время для пробуждения в объект времени
   wake_up = current_time.replace(hour=wake_up_hour, minute=wake_up_minute, second=0, microsecond=0)

   # Если введенное время для пробуждения уже прошло сегодня, добавляем 1 день
   if wake_up < current_time:
        wake_up += datetime.timedelta(days=1)
    
   # Вычисляем оптимальное время для засыпания, вычитая среднюю продолжительность сна (в часах)
   bedtime = wake_up - datetime.timedelta(hours=amount_hours)

   while bedtime < current_time:
      bedtime += datetime.timedelta(hours=1, minutes=30)
   
   bedtime.strftime("%H:%M")

   await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text=f"Оптимальное время для отхода ко сну это: {bedtime}"
      )

      


#FIXME
# Обработчик команды /calculate
'''async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):

   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Укажите желаемое время пробуждения в формате ЧЧ:ММ"
   )
   try:
      getting_values = put(Update)
      wake_up_hour, wake_up_minute = getting_values[0], getting_values[1]

      await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text="Отлично! Теперь укажите длительность сна, которую вы предпочитаете (в часах)."
      )

      hours = int(update.message.text)

      await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text=f"Указанное время: {hours}"
      )

   except:
      await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text="Извините, произошла ошибка. Пожалуйста, укажите время проснуться в формате ЧЧ:ММ."
      )'''

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Простите, я не знаю такой команды, повторите ваш запрос)")


def main():
   # Создание экземпляра Updater и передача токена вашего бота
   application = ApplicationBuilder().token('6060347607:AAFlBr6_tS7TrFjYlmfPHGcYPGyBbdr9LpA').build()
   
   start_handler = CommandHandler('start', start)
   application.add_handler(start_handler)

   '''if CHOICE == 0:
      application.'''
   
   cancel_handler = CommandHandler('cancel', cancel)


   # Run the bot until the user presses Ctrl-C
   application.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == '__main__':
   main()