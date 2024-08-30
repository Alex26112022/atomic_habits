from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """ Сериализатор для привычек. """

    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(ModelSerializer):
    """ Сериализатор для создания привычек. """

    class Meta:
        model = Habit
        fields = (
            'place', 'time', 'action', 'pleasant', 'related_habit', 'reward',
            'periodicity', 'time_to_complete', 'sign_of_publicity')

    def validate(self, attrs):
        """ Проверка на одновременное заполнение взаимоисключающих полей. """
        if attrs.get('pleasant') and attrs.get('related_habit') or attrs.get(
                'pleasant') and attrs.get('reward') or attrs.get(
                'reward') and attrs.get('related_habit'):
            raise serializers.ValidationError(
                'Может быть указано либо поле Приятная привычка, либо '
                'Связанная привычка, либо Вознаграждение!')
        return attrs
