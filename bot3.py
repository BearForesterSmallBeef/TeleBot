from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def close_keyboard(update, context):
    update.message.reply_text("клавиатура закрыта", reply_markup=ReplyKeyboardRemove())


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    update.message.reply_text("""Привет! Я эхо-бот. Я все повторяю! Что вы хотели?""",
                              reply_markup=markup)


def help(update, context):
    update.message.reply_text("""Я пока не умею помогать.""")


def main():
    updater = Updater('5165930033:AAE0WFGOJhipxcXXwpIkqEDQBpHjCkqxP2w',
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))

    dp.add_handler(CommandHandler("close", close_keyboard))
    text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


def address(update, context):
    update.message.reply_text("""Мой адрес не дом и не улица, мой адресс ссср""")


def phone(update, context):
    update.message.reply_text("""Телефон: +7(426)258-40-53""")


def site(update, context):
    update.message.reply_text("https://www.postman.com/")


def work_time(update, context):
    update.message.reply_text("Время работы: 9:00 - 20:00")


if __name__ == "__main__":
    main()
