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

CHOICE, TIME_OF_WAKEUP, HOURS = range(3)

wake_up_hour, wake_up_minute = 0, 0

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
   user = update.message.from_user
   logger.info("Choice of %s: %s", user.first_name, update.message.text)

   await context.bot.send_message(
      chat_id= update.effective_chat.id,
      text=f"Выбранная вами команда: {update.message.text}"
   )
   return CHOICE

async def getting_up_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Укажите желаемое время пробуждения в формате ЧЧ:ММ"
   )
   return TIME_OF_WAKEUP

async def getting_amountHours(update: Update, context: ContextTypes.DEFAULT_TYPE):
   string_fromUsers = update.message.text

   global wake_up_hour, wake_up_minute

   try:
      wake_up_hour, wake_up_minute = map(int, string_fromUsers.split(":"))
      
   except:
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Извините, произошла ошибка."
      )
      return CHOICE
   
   await context.bot.send_message(
         chat_id = update.effective_chat.id,
         text="Отлично! Теперь укажите длительность сна, которую вы предпочитаете (в часах)."
      )
   return HOURS

async def calculate_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):

   try:
      amount_hours = int(update.message.text)
   except:
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Извините, произошла ошибка. Пожалуйста, укажите длительность сна, которую вы предпочитаете (в часах)."
      )
      return TIME_OF_WAKEUP
   
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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await context.bot.send_message(
       chat_id= update.effective_chat.id,
       text= "Надеюсь, что я вам чем-то помог!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main():
   # Создание экземпляра Updater и передача токена вашего бота
   application = ApplicationBuilder().token('6060347607:AAFlBr6_tS7TrFjYlmfPHGcYPGyBbdr9LpA').build()
   
   conv_handler = ConversationHandler(
      entry_points=[CommandHandler("start", start)],
      states={
         CHOICE: [
            MessageHandler(
               filters.Regex("^Калькулятор сна$"), getting_up_time
            ),
            '''MessageHandler(
               filters.Regex("^Статьи"), articles
            ),
            MessageHandler(
               filters.Regex("^Промокод"), promo
            )'''
         ],
         TIME_OF_WAKEUP: [MessageHandler(filters.TEXT, getting_amountHours)],
         HOURS: [MessageHandler(filters.TEXT, calculate_hours)],
      },
      fallbacks=[CommandHandler("cancel", cancel)]
   )
   application.add_handler(conv_handler)
   
   # Run the bot until the user presses Ctrl-C
   application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
   main()