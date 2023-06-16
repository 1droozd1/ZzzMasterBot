from bot_methods import *
def main():
   # Создание экземпляра Updater и передача токена бота
   application = ApplicationBuilder().token(config.TOKEN).build()
   
   conv_handler = ConversationHandler(
      entry_points=[CommandHandler("start", start)],
      states={
         MAIN_MENU: [
            CallbackQueryHandler(main_menu, pattern="^(Давай начнем!|Назад в меню)$"),
            CallbackQueryHandler(cancel, pattern="^Пока$")
         ],
         CHOICE: [
            MessageHandler(
               filters.Regex("^Калькулятор сна$"), getting_up_time
            ),
            MessageHandler(
               filters.Regex("^Статьи"), article_command
            ),
            MessageHandler(
               filters.Regex(emoji.emojize("^Пока:waving_hand:$")), cancel
            ),
            '''
            MessageHandler(
               filters.Regex("^Промокод"), promo
            )'''
         ],
         TIME_OF_WAKEUP: [MessageHandler(filters.TEXT, getting_amountHours)],
         HOURS: [MessageHandler(filters.TEXT, calculate_hours)]
      },
      fallbacks=[MessageHandler(filters.Regex("^Пока$"), cancel)]
   )

   application.add_handler(conv_handler)
   application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
   main()