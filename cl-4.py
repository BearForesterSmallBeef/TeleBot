import random

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


def start(update, context):
    update.message.reply_text("Hello", reply_markup=start_markup)


def close_keyboard(update, context):
    update.message.reply_text("Возврат к главной клавиатуре", reply_markup=start_markup)


def checkout_dice(update, context):
    update.message.reply_text("Переключено на клавиатуру dice", reply_markup=dice_markup)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def task(context):
    job = context.job
    context.bot.send_message(job.context, text=f'{context.bot_data["due"]} истекло')


def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        if len(context.args) == 0:
            update.message.reply_text("Переключено на клавиатуру timer", reply_markup=timer_markup)
        else:
            due = int(context.args[0])
            if len(context.args) >= 2:
                if context.args[1].lower() in ["min", "mins"]:
                    due *= 60
            if due < 0:
                update.message.reply_text('Извините, не умеем возвращаться в прошлое')
                return

            context.bot_data["due"] = due
            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

            text = f'засек {due}'
            if job_removed:
                text += 'Таймер сброшен'
            update.message.reply_text(text, reply_markup=close_timer_markup)
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /timer <секунд>')


def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    update.message.reply_text(text, reply_markup=timer_markup)


def echo(update, context):
    update.message.reply_text("Команда нераспознана")


def main():
    updater = Updater('5165930033:AAE0WFGOJhipxcXXwpIkqEDQBpHjCkqxP2w',
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("timer",
                                  set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("roll_the_dice",
                                  roll_the_dice,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("dice", checkout_dice))

    dp.add_handler(CommandHandler("back", close_keyboard))
    dp.add_handler(CommandHandler("close", close,
                                  pass_chat_data=True))

    text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


def roll_the_dice(update, context):
    text = "Ошибка"
    if len(context.args) == 1:
        text = " ".join([str(random.randrange(1, int(context.args[0]) + 1)) for _ in range(1)])
    if len(context.args) >= 2:
        text = " ".join([str(random.randrange(1, int(context.args[0]) + 1)) for _ in range(int(context.args[1]))])
    update.message.reply_text(text)


if __name__ == "__main__":
    main()
