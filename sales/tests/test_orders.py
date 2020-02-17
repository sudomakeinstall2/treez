from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from sales.models import Order, Inventory


class OrderListTestCase(APITestCase):

    def setUp(self):
        self.user = mommy.make(User, email="a@b.com")
        self.inv = mommy.make(Inventory)

    def test_order_list(self):
        order = mommy.make(Order, customer=self.user, inventories=[self.inv])
        data = {
            "id": order.id,
            "customer": self.user.email,
            "status": order.status,
            "inventories": [self.inv.id]
        }
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        json = response.json()[0]
        json.pop('created_at')
        self.assertDictEqual(data, json)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            "customer": self.user.email,
            "status": "created",
            "inventories": [self.inv.id, ],
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.filter(customer__email=data['customer']).first()
        self.assertDictEqual({
            "customer": order.customer.email,
            "status": order.status,
            "inventories": [o.id for o in order.inventories.all()],
        }, data)
