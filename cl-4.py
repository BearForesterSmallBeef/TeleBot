from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


start_keyboard = [["/dice", "/timer"],
                  ["/back"]]

dice_keyboard = [["/roll_the_dice 6", "/roll_the_dice 6 2", "/roll_the_dice 20"],
                 ["/back"]]

timer_keyboard = [["/timer 30", "/timer 1 min", "/timer 5 min"],
                  ["/back"]]

close_timer_keyboard = [["/close"]]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
close_timer_markup = ReplyKeyboardMarkup(close_timer_keyboard, one_time_keyboard=False)


def close_keyboard(update, context):
    update.message.
    update.message.reply_text("клавиатура закрыта", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("клавиатура закрыта", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("клавиатура закрыта", reply_markup=ReplyKeyboardRemove())

    update.message.reply_text("клавиатура закрыта", reply_markup=ReplyKeyboardRemove())

