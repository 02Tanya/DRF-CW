from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    time = '13:19:00'

    def setUp(self):
        # self.client = APIClient()
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action='Habit_test1',
            periodicity=1,
            lead_time='10',
            time=self.time,
            is_public=True
        )

        self.habit_pleasurable = Habit.objects.create(
            user=self.user,
            action='Habit_test1_pleasurable',
            periodicity=1,
            lead_time='10',
            time=self.time,
            is_pleasurable=True,
        )

    def test_create_habit(self):
        '''Тестирование создания привычки'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test2",
            "lead_time": 10,
            "periodicity": 1,
            "time": self.time
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)


    def test_create_habit_validation_error_1(self):
        '''Тестирование проверки времени на выполнение привычки'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test2",
            "lead_time": 121,
            "periodicity": 1,
            "time": self.time
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Время выполнения привычки - не более 120 сек."
                ]
            }
        )

    def test_create_habit_validation_error_2(self):
        '''Тестирование проверки периодичности выполнения в днях'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test2",
            "lead_time": 10,
            "periodicity": 8,
            "time": self.time
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Привычку надо выполнять не реже, чем 1 раз за 7 дней"
                ]
            }
        )

    def test_create_habit_validation_error_3(self):
        '''Тестирование проверки, что одновременно не назначено вознаграждение и связанная привычка'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "associated_habit": self.habit_pleasurable.id,
            "reward": "Test"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя назначать вознаграждение и связанную привычку вместе"
                ]
            }
        )

    def test_create_habit_validation_error_4(self):
        '''Тестирование проверки, что у приятной привычки не назначено вознаграждение или связанная привычка'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "is_pleasurable": True,
            "associated_habit": self.habit_pleasurable.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя назначать вознаграждение или связанную привычку для приятной привычки"
                ]
            }
        )

    def test_create_habit_validation_error_5(self):
        '''Тестирование проверки, что связанная привычка является приятной'''
        url = reverse("habits:habit_create")
        data = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "associated_habit": self.habit.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Связанная привычка должна быть приятной"
                ]
            }
        )

    def test_retrieve_habit(self):
        '''Тестирование возможности просмотра привычки'''
        response = self.client.get(f'/habits/{self.habit.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': None,
                'time': '13:19:00',
                'periodicity': 1,
                'action': 'Habit_test1',
                'is_pleasurable': False,
                'associated_habit': None,
                'reward': None,
                'lead_time': 10,
                'is_public': True
            }
        )

    def test_list_habit(self):
        '''Тестирование вывода списка привычек'''
        url = reverse("habits:habits_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results':
                 [
                     {
                         'id': self.habit.id,
                         'place': None,
                         'time': '13:19:00',
                         'periodicity': 1,
                         'action': 'Habit_test1',
                         'is_pleasurable': False,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10,
                         'is_public': True
                     },
                     {
                         'id': self.habit_pleasurable.id,
                         'place': None,
                         'time': '13:19:00',
                         'periodicity': 1,
                         'action': 'Habit_test1_pleasurable',
                         'is_pleasurable': True,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10,
                         'is_public': False
                     }
                 ]
             }
        )

    def test_public_list_habit(self):
        '''Тестирование вывода списка публичных привычек'''
        url = reverse("habits:habits-public_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results':
                 [
                     {
                         'place': None,
                         'time': '13:19:00',
                         'periodicity': 1,
                         'action': 'Habit_test1',
                         'is_pleasurable': False,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10
                     }
                 ]
             }
        )

    def test_update_habit(self):
        '''Тестирование обновления привычки'''

        habit = {
            "action": "Habit_test1_update",
            "lead_time": 10,
            "periodicity": 1,
            "time": self.time,
            "is_public": True
        }

        response = self.client.patch(
            f'/habits/{self.habit.id}/update/',
            data=habit
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': None,
                'time': '13:19:00',
                'periodicity': 1,
                'action': 'Habit_test1_update',
                'is_pleasurable': False,
                'associated_habit': None,
                'reward': None,
                'lead_time': 10,
                'is_public': True
            }
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        response = self.client.delete(
            f'/habits/{self.habit.id}/delete/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
