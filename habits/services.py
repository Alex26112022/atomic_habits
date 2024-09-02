import json
import zoneinfo
from datetime import datetime, timedelta

import requests
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from config.settings import TIME_ZONE, TELEGRAM_TOKEN, TELEGRAM_URL, \
    FIRST_INTERVAL, SECOND_INTERVAL


def habit_send_tg(message, chat_id):
    """ Отправляет текущие привычки в Telegram."""
    if chat_id:
        params = {
            'text': message,
            'chat_id': chat_id,
        }
        requests.get(
            f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage',
            params=params)
        print(message, chat_id)
    else:
        print(message, 'telegram_chat_id не указан!')


def create_periodical_task(pk, place, time_: datetime, action, related_habit,
                           reward, periodicity, time_to_complete, chat_id):
    """ Создает периодическую задачу. """
    name = str(pk)

    hour = '*'
    minute = '*'

    delta_time1 = timedelta(minutes=FIRST_INTERVAL)
    delta_time2 = timedelta(minutes=SECOND_INTERVAL)
    if time_:
        dt = datetime(year=2024, month=10, day=10, hour=time_.hour,
                      minute=time_.minute)

        correction_time1 = (dt - delta_time1).time()
        correction_time2 = (dt - delta_time2).time()
        current_time1 = correction_time1.strftime('%H:%M').split(':')
        current_time2 = correction_time2.strftime('%H:%M').split(':')
        hour1 = current_time1[0]
        minute1 = current_time1[1]
        hour2 = current_time2[0]
        minute2 = current_time2[1]

        hour = hour1 + ',' + hour2
        minute = minute1 + ',' + minute2

    day = '*'
    if periodicity and periodicity != 1:
        day = f'*/{str(periodicity)}'

    message = (f'Действие: {action}\nМесто проведения: {place}\n'
               f'Время проведения: {time_}\n'
               f'Продолжительность: {time_to_complete} c.\n')
    if related_habit:
        message += f'Связанная привычка: {related_habit}'
    elif reward:
        message += f'Вознаграждение: {reward}'

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_month=day,
        timezone=zoneinfo.ZoneInfo(TIME_ZONE))

    PeriodicTask.objects.create(
        crontab=schedule,
        name=name,
        task="habits.tasks.task_send_tg",
        args=json.dumps([message, chat_id])
    )


def update_periodical_task(pk, place, time_: datetime, action, related_habit,
                           reward, periodicity, time_to_complete, chat_id):
    """ Редактирует периодическую задачу. """
    if PeriodicTask.objects.filter(name=str(pk)).exists():
        periodic_task = PeriodicTask.objects.get(name=str(pk))

        hour = '*'
        minute = '*'

        delta_time1 = timedelta(minutes=FIRST_INTERVAL)
        delta_time2 = timedelta(minutes=SECOND_INTERVAL)
        if time_:
            dt = datetime(year=2024, month=10, day=10, hour=time_.hour,
                          minute=time_.minute)

            correction_time1 = (dt - delta_time1).time()
            correction_time2 = (dt - delta_time2).time()
            current_time1 = correction_time1.strftime('%H:%M').split(':')
            current_time2 = correction_time2.strftime('%H:%M').split(':')
            hour1 = current_time1[0]
            minute1 = current_time1[1]
            hour2 = current_time2[0]
            minute2 = current_time2[1]

            hour = hour1 + ',' + hour2
            minute = minute1 + ',' + minute2

        day = '*'
        if periodicity and periodicity != 1:
            day = f'*/{str(periodicity)}'

        message = (f'Действие: {action}\nМесто проведения: {place}\n'
                   f'Время проведения: {time_}\n'
                   f'Продолжительность: {time_to_complete} c.\n')
        if related_habit:
            message += f'Связанная привычка: {related_habit}'
        elif reward:
            message += f'Вознаграждение: {reward}'

        periodic_task.crontab.minute = minute
        periodic_task.crontab.hour = hour
        periodic_task.crontab.day_of_month = day
        periodic_task.crontab.save()
        periodic_task.args = json.dumps([message, chat_id])
        periodic_task.save()
