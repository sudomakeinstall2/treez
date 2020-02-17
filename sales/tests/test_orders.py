from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from sales.models import Order, Inventory


class OrderListTestCase(APITestCase):

    def setUp(self):
        pass

    def test_order_list(self):
        user = mommy.make(User, email="a@b.com")
        inv = mommy.make(Inventory)
        order = mommy.make(Order, customer=user, inventories=[inv])
        data = {
            "id": order.id,
            "customer": user.email,
            "status": order.status,
            "inventories": [inv.id]
        }
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        json = response.json()[0]
        json.pop('created_at')
        self.assertDictEqual(data, json)
