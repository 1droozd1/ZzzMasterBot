import logging
from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update, 
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import datetime

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

articles = {
   "First" : "https://github.com/1droozd1",
   "Second" : "https://github.com/1droozd1",
   "Third" : "https://github.com/1droozd1",
   "Fourth" : "https://github.com/1droozd1",
   "Fifth" : "https://github.com/1droozd1",
}

# Настройка журналирования
logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOICE, TIME_OF_WAKEUP, HOURS, ARTICLE, BUTTON = range(5)

wake_up_hour, wake_up_minute = 0, 0

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   reply_keyboard_first_menu = [["Калькулятор сна", "Статьи", "Промокод"]]

   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = """Привет! Я могу помочь тебе определить оптимальное время для засыпания и пробуждения. Выбери один из предложенных вариантов моих функций.""",
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_first_menu,
         resize_keyboard=True,
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
         text=f"Оптимальное время для отхода ко сну это: {bedtime}",
         
   )

   return CHOICE

async def article_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

   keyboard = [
            [InlineKeyboardButton(f"{key}", callback_data=f"{value}", url=value)] for key, value in articles.items() 
   ]

   #print(keyboard)
   reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Выберите из предложенного списка интересующую вас статью:",
      reply_markup=reply_markup
   )
   return BUTTON

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


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
            MessageHandler(
               filters.Regex("^Статьи"), article_command
            ),
            '''
            MessageHandler(
               filters.Regex("^Промокод"), promo
            )'''
         ],
         TIME_OF_WAKEUP: [MessageHandler(filters.TEXT, getting_amountHours)],
         HOURS: [MessageHandler(filters.TEXT, calculate_hours)],
         BUTTON: [CallbackQueryHandler(button)]
      },
      fallbacks=[CommandHandler("cancel", cancel)]
   )
   application.add_handler(conv_handler)
   
   # Run the bot until the user presses Ctrl-C
   application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
   main()