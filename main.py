import random

from environs import Env
import pytimeparse

import ptbot


def format_progress_message(seconds_total, seconds_left):
    return render_progressbar(
        total = seconds_total,
        iteration = seconds_total - seconds_left,
        prefix = f"Осталось {seconds_left} секунд\n"
    )


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| \n{2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(seconds_left, seconds_total, message_id):
    bot.update_message(
        tg_chat_id, message_id, format_progress_message(seconds_total, seconds_left)
    )


def notify_time_is_over():
    bot.send_message(tg_chat_id, "Время вышло!")


def reply(time):
    parsed_time = pytimeparse.parse(time)
    if parsed_time is None:
        error_message = 'Я так не понимаю.\nНапишите что-то вроде "5s" или "1.2 minutes"'
        bot.send_message(tg_chat_id, error_message)
        return
    message_id = bot.send_message(
        tg_chat_id, format_progress_message(parsed_time, parsed_time)
    )
    bot.create_countdown(parsed_time, notify_progress, parsed_time, message_id)
    bot.create_timer(parsed_time, notify_time_is_over)


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    tg_token = env.str("tg_token")
    tg_chat_id = env.int("tg_chat_id")

    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, "На какое время поставить таймер?")
    bot.reply_on_message(reply)
    bot.run_bot()
