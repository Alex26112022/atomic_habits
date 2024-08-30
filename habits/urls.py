from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListApiView, HabitRetrieveApiView, \
    HabitCreateApiView, HabitUpdateApiView, HabitDestroyApiView, \
    HabitPublicListApiView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListApiView.as_view(), name='habits_list'),
    path('habit/<int:pk>/', HabitRetrieveApiView.as_view(),
         name='habit_detail'),
    path('habit/create/', HabitCreateApiView.as_view(), name='habit_create'),
    path('habit/<int:pk>/update/', HabitUpdateApiView.as_view(),
         name='habit_update'),
    path('habit/<int:pk>/delete/', HabitDestroyApiView.as_view(),
         name='habit_delete'),
    path('habits-public/', HabitPublicListApiView.as_view(),
         name='habits_public_list'),
]
