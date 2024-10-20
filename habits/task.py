import datetime
import os

import requests
from celery import shared_task

from habits.models import Habit


@shared_task
def send_message():
    now = datetime.datetime.now()

    habits = Habit.objects.all()
    for habit in habits:
        if habit.date_of_next_reminder_sending is None:
            habit.date_of_next_reminder_sending = now.date()

        if (habit.date_of_next_reminder_sending <= now.date()
                and habit.time.hour == now.hour):
            chat_id = habit.user.telegram_chat_id
            if chat_id is None:
                message = (
                    f'Напоминание выполнить {habit.action} в {habit.time} в {habit.place}')
                url = f"https://api.telegram.org/bot{os.getenv('API_KEY_TELEGRAM_BOT')}/" \
                      f"sendMessage?chat_id={chat_id}&text={message}"
                requests.post(url).json()

                habit.date_of_next_reminder_sending += datetime.timedelta(
                    days=habit.periodicity)
                habit.save()
