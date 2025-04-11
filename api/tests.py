from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status
# Create your tests here.

class UserOrderTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='user1',password='12345')
        u2 = User.objects.create_user(username='user2',password='12345')
        Order.objects.create(user=u1)
        Order.objects.create(user=u1)
        Order.objects.create(user=u2)
        Order.objects.create(user=u2)

    def test_authicated_user_order(self):

        u1 = User.objects.get(username="user1")
        self.client.force_login(user=u1)
        response = self.client.get(reverse("user-orders"))
        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        print(orders)
        self.assertTrue(all(order["user"] == u1.pk for order in orders))

    def test_unauthenticated_user_order(self):

        response = self.client.get(reverse("user-orders"))
        assert response.status_code == status.HTTP_403_FORBIDDEN
