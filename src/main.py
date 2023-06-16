from bot_methods import *
def main():
   # Создание экземпляра Updater и передача токена вашего бота
   application = ApplicationBuilder().token(config.TOKEN).build()
   
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
         #BUTTON: [CallbackQueryHandler(button)] - Возможно пригодится
      },
      fallbacks=[CommandHandler("cancel", cancel)]
   )

   application.add_handler(conv_handler)
   application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
   main()