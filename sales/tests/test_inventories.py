from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from sales.models import Inventory


class InventoryListTestCase(APITestCase):

    def setUp(self):
        self.inventory = mommy.make(Inventory)

    def test_inventory_list(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        expected = {
            "name": self.inventory.name,
            "description": self.inventory.description,
            "price": self.inventory.price,
            "quantity": self.inventory.quantity,
            "id": self.inventory.id,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(response.json()[0], expected)
