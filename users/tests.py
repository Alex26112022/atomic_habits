from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        pass

    def test_login_refresh(self):
        url1 = reverse('users:user_create')
        url2 = reverse('users:login')
        url3 = reverse('users:refresh')
        data1 = {'username': 'testuser',
                 'password': 1234}

        self.client.post(url1, data=data1)
        response2 = self.client.post(url2, data=data1)

        data2 = {'refresh': response2.data.get('refresh')}

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response2.data.get('access'), None)
        self.assertNotEqual(response2.data.get('refresh'), None)

        response3 = self.client.post(url3, data=data2)

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response3.data.get('access'), None)

    def test_user_create_get(self):
        url1 = reverse('users:user_create')
        url2 = reverse('users:user_list')
        data = {'username': 'testuser2',
                'password': 1234}
        response1 = self.client.post(url1, data=data)
        user = User.objects.all().first()
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.client.force_authenticate(user=user)

        response2 = self.client.get(url2)
        data_ = response2.json()

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(data_[0].get('username'), 'testuser2')

    def test_user_detail_update_delete(self):
        url1 = reverse('users:user_create')
        data = {'username': 'testuser3',
                'password': 1234}
        response1 = self.client.post(url1, data=data)
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)

        url2 = reverse('users:user_detail', args=(response1.data.get('id'),))
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get('username'), 'testuser3')

        url3 = reverse('users:user_update', args=(response1.data.get('id'),))
        data2 = {'username': 'newtestuser3'}
        response3 = self.client.patch(url3, data=data2)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data.get('username'),
                         'newtestuser3')

        url4 = reverse('users:user_delete', args=(response1.data.get('id'),))
        response4 = self.client.delete(url4)
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
