from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(owner=self.user,
                                          place='Test place',
                                          time='13:45:12',
                                          action='test action',
                                          pleasant=None,
                                          related_habit=None,
                                          reward='test reward',
                                          periodicity=3,
                                          time_to_complete=90,
                                          sign_of_publicity=True)

    def test_get_habit(self):
        url = reverse('habits:habits_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_habit_detail(self):
        url = reverse('habits:habit_detail', args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create(self):
        url = reverse('habits:habit_create')
        data = {'owner': self.user.pk,
                'place': 'Test place2',
                'time': '14:45:12',
                'action': 'test action2',
                'reward': 'test reward2',
                'periodicity': 3,
                'time_to_complete': 90,
                'sign_of_publicity': True}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_update(self):
        url = reverse('habits:habit_update', args=(self.habit.pk,))
        data = {'owner': self.user.pk,
                'place': 'Updated Test place',
                'time': '15:45:12',
                'action': 'updated test action',
                'reward': 'updated test reward',
                'periodicity': 3,
                'time_to_complete': 90,
                'sign_of_publicity': True}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        url = reverse('habits:habit_delete', args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
