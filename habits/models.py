from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User

options = {'blank': True, 'null': True}


class Habit(models.Model):
    """ Модель привычки. """
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='habit',
                              verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место', **options)
    time = models.TimeField(verbose_name='Время', **options)
    action = models.CharField(max_length=255, verbose_name='Действие',
                              **options)
    pleasant = models.BooleanField(verbose_name='Приятная привычка', **options)
    related_habit = models.CharField(max_length=255,
                                     verbose_name='Связанная привычка',
                                     **options)
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение',
                              **options)
    periodicity = models.PositiveIntegerField(verbose_name='Периодичность',
                                              default=1,
                                              validators=[
                                                  MaxValueValidator(7)],
                                              **options)
    time_to_complete = models.PositiveIntegerField(
        verbose_name='Время на выполнение',
        validators=[MaxValueValidator(120)],
        **options)
    sign_of_publicity = models.BooleanField(default=False,
                                            verbose_name='Признак публичности',
                                            **options)

    def __str__(self):
        return f'{self.owner} - {self.place} - {self.action}'

    def save(
            self, *args, force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        if self.pleasant and self.related_habit or self.pleasant and self.reward or self.reward and self.related_habit:
            raise ValueError(
                'Может быть указано либо поле Приятная привычка, либо Связанная привычка, либо Вознаграждение!')
        super().save(*args, force_insert=False, force_update=False, using=None,
                     update_fields=None)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
