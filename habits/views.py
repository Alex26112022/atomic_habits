from django_celery_beat.models import PeriodicTask
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
from habits.models import Habit
from habits.paginators import MyPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitCreateSerializer
from habits.services import create_periodical_task, update_periodical_task


class HabitCreateApiView(CreateAPIView):
    """ Создает новую привычку. """
    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)
        habit.save()

        create_periodical_task(pk=habit.pk, place=habit.place,
                               time_=habit.time,
                               action=habit.action,
                               related_habit=habit.related_habit,
                               reward=habit.reward,
                               periodicity=habit.periodicity,
                               time_to_complete=habit.time_to_complete,
                               chat_id=habit.owner.telegram_chat_id)


class HabitListApiView(ListAPIView):
    """ Возвращает список всех привычек. """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)


class HabitRetrieveApiView(RetrieveAPIView):
    """ Возвращает информацию о привычке. """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)


class HabitUpdateApiView(UpdateAPIView):
    """ Редактирует привычку. """
    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        habit.save()

        update_periodical_task(pk=habit.pk, place=habit.place,
                               time_=habit.time,
                               action=habit.action,
                               related_habit=habit.related_habit,
                               reward=habit.reward,
                               periodicity=habit.periodicity,
                               time_to_complete=habit.time_to_complete,
                               chat_id=habit.owner.telegram_chat_id)


class HabitDestroyApiView(DestroyAPIView):
    """ Удаляет привычку. """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

    def perform_destroy(self, instance):
        task_name = str(instance.id)
        periodic_task = PeriodicTask.objects.get(name=str(task_name))
        periodic_task.crontab.delete()
        periodic_task.delete()
        instance.delete()


class HabitPublicListApiView(ListAPIView):
    """ Возвращает список всех публичных привычек. """
    queryset = Habit.objects.filter(sign_of_publicity=True)
    serializer_class = HabitSerializer
    pagination_class = MyPaginator
