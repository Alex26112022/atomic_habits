from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Habit
from habits.paginators import MyPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitCreateSerializer


class HabitCreateApiView(CreateAPIView):
    """ Создает новую привычку. """
    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)
        habit.save()


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


class HabitDestroyApiView(DestroyAPIView):
    """ Удаляет привычку. """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitPublicListApiView(ListAPIView):
    """ Возвращает список всех публичных привычек. """
    queryset = Habit.objects.filter(sign_of_publicity=True)
    serializer_class = HabitSerializer
    pagination_class = MyPaginator
