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
            "inventories": [self.inv.id],
            "created_at": datetime_representation(order.created_at),
        }
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertDictEqual(data, response.json()[0])

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

    def test_create_order_decrease_inventory_quantity(self):
        url = reverse('order-list')
        data = {
            "customer": self.user.email,
            "status": "created",
            "inventories": [self.inv.id, self.inv.id],
        }
        quantity_before = self.inv.quantity
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.inv.refresh_from_db()
        self.assertEqual(self.inv.quantity + 2, quantity_before)

    def test_cant_create_order_more_than_inventory_quantity(self):
        url = reverse('order-list')
        data = {
            "customer": self.user.email,
            "status": "created",
            "inventories": [self.inv.id],
        }
        self.inv.quantity = 0
        self.inv.save()

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderDetailTestCase(APITestCase):

    def setUp(self):
        self.user = mommy.make(User, email="a@b.com")
        self.inv = mommy.make(Inventory)
        self.order = mommy.make(
            Order, customer=self.user, inventories=[self.inv], status=Order.CREATED
        )

    def test_get_order(self):
        url = reverse('order-detail', args=(self.order.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {
            "customer": self.order.customer.email,
            "status": self.order.status,
            "inventories": [o.id for o in self.order.inventories.all()],
            "created_at": datetime_representation(self.order.created_at),
            "id": self.order.id
        })

    def test_change_inventories(self):
        new_inventory = mommy.make(Inventory)
        url = reverse('order-detail', args=(self.order.id,))
        data = {
            "inventories": [new_inventory.id],
            "status": self.order.status,
        }
        old_inventory_quantity_before = self.inv.quantity
        new_inventory_quantity_before = new_inventory.quantity
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {
            "status": data["status"],
            "inventories": [new_inventory.id],
            "created_at": datetime_representation(self.order.created_at),
            "id": self.order.id
        })
        self.inv.refresh_from_db()
        new_inventory.refresh_from_db()
        self.assertEqual(old_inventory_quantity_before + 1, self.inv.quantity)
        self.assertEqual(new_inventory_quantity_before - 1, new_inventory.quantity)

    def test_update_status_cancelled_and_finished(self):
        self.order.status = Order.CANCELLED
        self.order.save()
        url = reverse('order-detail', args=(self.order.id,))
        data = {
            "inventories": [self.inv.id],
            "status": Order.CREATED,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.order.status = Order.FINISHED
        self.order.save()
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_increase_inventory_on_cancel(self):
        url = reverse('order-detail', args=(self.order.id,))
        data = {
            "inventories": [self.inv.id],
            "status": Order.CANCELLED,
        }
        quantity_before = self.inv.quantity
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.inv.refresh_from_db()
        self.assertEqual(quantity_before + 1, self.inv.quantity)

    def test_delete_order(self):
        url = reverse('order-detail', args=(self.order.id,))
        quantity_before = self.inv.quantity
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=self.order.id)
        self.inv.refresh_from_db()
        self.assertEqual(quantity_before + 1, self.inv.quantity)


def datetime_representation(datetime):
    value = datetime.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value
