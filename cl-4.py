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
    update.message.reply_text("Возврат к главной клавиатуре", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(reply_markup=start_markup)


def checkout_dice(update, context):
    update.message.reply_text(reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(reply_markup=dice_markup)


def checkout_timer(update, context):
    update.message.reply_text(reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(reply_markup=timer_markup)


def checkout_close(update, context):
    update.message.reply_text(reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(reply_markup=close_timer_markup)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='КУКУ!')


def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if len(context.args >= 2):
            if context.args[1].lower() in ["min", "mins"]:
                due *= 60
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')