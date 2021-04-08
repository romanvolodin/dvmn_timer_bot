import random

from environs import Env
import pytimeparse

import ptbot


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| \n{2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(seconds_left, seconds_total, message_id):
    bot.update_message(TG_CHAT_ID, message_id, render_progressbar(
        total = seconds_total,
        iteration = seconds_total - seconds_left
    ))


def notify_time_is_over():
    bot.send_message(TG_CHAT_ID, "Время вышло!")


def reply(time):
    parsed_time = pytimeparse.parse(time)
    if parsed_time is None:
        error_message = 'Я так не понимаю.\nНапишите что-то вроде "5s" или "1.2 minutes"'
        bot.send_message(TG_CHAT_ID, error_message)
        return
    message_id = bot.send_message(TG_CHAT_ID, render_progressbar(parsed_time, 0))
    bot.create_countdown(parsed_time, notify_progress, parsed_time, message_id)
    bot.create_timer(parsed_time, notify_time_is_over)


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    TG_TOKEN = env.str("TG_TOKEN")
    TG_CHAT_ID = env.int("TG_CHAT_ID")

    bot = ptbot.Bot(TG_TOKEN)
    bot.send_message(TG_CHAT_ID, "На какое время поставить таймер?")
    bot.reply_on_message(reply)
    bot.run_bot()
