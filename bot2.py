from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    update.message.reply_text("""Привет! Я эхо-бот. Я все повторяю!""")


def help(update, context):
    update.message.reply_text("""Я пока не умею помогать.""")


def main():
    updater = Updater('5165930033:AAE0WFGOJhipxcXXwpIkqEDQBpHjCkqxP2w',
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()