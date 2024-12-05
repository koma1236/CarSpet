from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from cars.models import Car
from comments.models import Comment


class CarAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'testuser@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.car1 = Car.objects.create(make='Toyota', model='Corolla', year=2015, description='Good car',
                                       owner=self.user)
        self.car2 = Car.objects.create(make='Honda', model='Civic', year=2010, description='Excellent car',
                                       owner=self.user)

    def test_get_all_cars(self):
        response = self.client.get(reverse('cars-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_valid_car(self):
        response = self.client.get(reverse('cars-detail', kwargs={'pk': self.car1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['make'], 'Toyota')

    def test_get_invalid_car(self):
        response = self.client.get(reverse('cars-detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_car(self):
        data = {
            'make': 'Nissan',
            'model': 'Altima',
            'year': 2018,
            'description': 'New car',
            'owner': self.user.id
        }
        response = self.client.post(reverse('cars-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 3)

    def test_create_invalid_car(self):
        data = {'make': '', 'model': '', 'year': 2018, 'description': 'New car'}
        response = self.client.post(reverse('cars-list'), data, format='json')  # Исправлено на 'cars-list'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_car(self):
        data = {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2015,
            'description': 'Good car',
            'owner': self.user.id
        }
        response = self.client.put(reverse('cars-detail', kwargs={'pk': self.car1.pk}), data, format='json')

        if response.status_code != status.HTTP_200_OK:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['model'], 'Camry')

    def test_update_invalid_car(self):
        data = {'make': '', 'model': '', 'year': 2018, 'description': 'New car'}
        response = self.client.put(reverse('cars-detail', kwargs={'pk': self.car1.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_car(self):
        response = self.client.delete(reverse('cars-detail', kwargs={'pk': self.car1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 1)

    def test_delete_invalid_car(self):
        response = self.client.delete(reverse('cars-detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentAPITestCase(APITestCase):
    def setUp(self):
        # Создаем суперпользователя для тестирования
        self.user = User.objects.create_superuser('testuser', 'testuser@gmail.com', 'password')
        # Аутентификация пользователя для всех тестов
        self.client.force_authenticate(user=self.user)
        # Создаем автомобиль для тестирования
        self.car = Car.objects.create(make='Toyota', model='Corolla', year=2015, description='Good car',
                                      owner=self.user)

    def test_get_comments_for_car(self):
        # Тестируем получение комментариев к автомобилю
        Comment.objects.create(car=self.car, author=self.user, content='Great car!')  # Создаем комментарий

        # отправляем GET-запрос для получения комментариев
        response = self.client.get(reverse('car-comments', kwargs={'car_id': self.car.id}))  # Используем car_id
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что статус ответа 200 (OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что в ответе один комментарий
        self.assertEqual(response.data[0]['content'], 'Great car!')  # Проверяем текст комментария

    def test_post_comment_to_car(self):
        # Тестируем добавление нового комментария к автомобилю
        data = {
            'content': 'This car is amazing!',  # Текст комментария
            'car': self.car.id  # Идентификатор автомобиля
        }
        response = self.client.post(reverse('car-comments', kwargs={'car_id': self.car.id}), data,
                                    format='json')  # Отправляем POST-запрос для создания комментария

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что статус ответа 201 (Created)
        self.assertEqual(Comment.objects.count(), 1)  # Проверяем, что количество комментариев увеличилось на 1
        self.assertEqual(Comment.objects.first().content, 'This car is amazing!')  # Проверяем текст комментария
        self.assertEqual(Comment.objects.first().author, self.user)  # Проверяем, что автор комментария правильный
