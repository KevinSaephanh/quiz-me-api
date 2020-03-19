from users.models import CustomUser
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.views import UserViewSet


class UserViewSetTestCase(APITestCase):

    page_list_url = reverse('api/users/page=1')

    def setUp(self):
        CustomUser.objects._create_user(
            username='TestUser1', email='Test1@email.com', password='Test123')
        CustomUser.objects._create_user(
            username='TestUser2', email='Test2@email.com', password='Test123')
        CustomUser.objects._create_user(
            username='TestUser3', email='Test3@email.com', password='Test123')

    def test_paginated_user_list(self):
        response = self.client.get(self.page_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        response = self.client.get(reverse('api/users/', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'TestUser1')
