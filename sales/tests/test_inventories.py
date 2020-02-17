from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from sales.models import Inventory


class InventoryListTestCase(APITestCase):

    def setUp(self):
        pass

    def test_inventory_list(self):
        inventory = mommy.make(Inventory)
        url = reverse('inventory-list')
        response = self.client.get(url)
        expected = {
            "name": inventory.name,
            "description": inventory.description,
            "price": inventory.price,
            "quantity": inventory.quantity,
            "id": inventory.id,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(response.json()[0], expected)

    def test_inventory_create(self):
        url = reverse('inventory-list')
        data = {
            "name": "name",
            "description": "desc",
            "price": 1242,
            "quantity": 20
        }
        response = self.client.post(url, data=data)
        inventory = Inventory.objects.get(name=data['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual({
            "name": inventory.name,
            "description": inventory.description,
            "price": inventory.price,
            "quantity": inventory.quantity
        }, data)
