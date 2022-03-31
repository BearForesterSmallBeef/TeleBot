from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import datetime


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    update.message.reply_text("""Привет! Я эхо-бот. Я все повторяю!""")


def help(update, context):
    update.message.reply_text("""Я пока не умею помогать.""")


def time(update, context):
    update.message.reply_text(str(datetime.datetime.now().time()))


def date(update, context):
    update.message.reply_text(str(datetime.datetime.now().date()))


def main():
    updater = Updater('5165930033:AAE0WFGOJhipxcXXwpIkqEDQBpHjCkqxP2w',
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("date", date))
    text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
