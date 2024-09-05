from rest_framework import serializers
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
        """ Проверка полей. """
        if attrs.get('pleasant') and attrs.get('related_habit') or attrs.get(
                'pleasant') and attrs.get('reward') or attrs.get('reward') and attrs.get('related_habit'):  # noqa
            raise serializers.ValidationError(
                'Может быть указано либо поле Приятная привычка, либо '
                'Связанная привычка, либо Вознаграждение!')
        if attrs.get('related_habit'):
            related_habit = attrs.get('related_habit')
            if related_habit.owner != self.context.get('request').user:
                raise serializers.ValidationError(
                    'Связанная привычка не принадлежит текущему пользователю.')  # noqa
            if not related_habit.pleasant:
                raise serializers.ValidationError(
                    'Связанная привычка не является приятной.')
        return attrs
