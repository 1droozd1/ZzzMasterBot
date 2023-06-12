import logging
from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
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
      text = """Привет! Я могу помочь тебе определить оптимальное время для засыпания и пробуждения. 
      Напиши \calculate для вычисления оптимального времени пробуждения"""
   )

async def put(update: Update) -> list:
    value = list(map(int, update.message.text.split(":")))
    return value

# Обработчик команды /calculate
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
      )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Простите, я не знаю такой команды, повторите ваш запрос)")


def main():
   # Создание экземпляра Updater и передача токена вашего бота
   application = ApplicationBuilder().token('6060347607:AAFlBr6_tS7TrFjYlmfPHGcYPGyBbdr9LpA').build()
    
   start_handler = CommandHandler('start', start)
   application.add_handler(start_handler)

   calculate_handler = CommandHandler('calculate', calculate)
   application.add_handler(calculate_handler)

   unknown_handler = MessageHandler(filters.COMMAND, unknown)
   application.add_handler(unknown_handler)
    
   application.run_polling()
    

if __name__ == '__main__':
   main()