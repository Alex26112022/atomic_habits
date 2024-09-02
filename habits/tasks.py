from celery import shared_task

from habits.services import habit_send_tg


@shared_task
def task_send_tg(message, chat_id):
    """ Задача для отправки сообщения в Telegram. """
    habit_send_tg(message, chat_id)
