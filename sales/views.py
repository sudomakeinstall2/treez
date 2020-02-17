from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .serializers import InventorySerializer, OrderSerializer, UpdateOrderSerializer
from .models import Inventory, Order


class InventoryListView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def perform_destroy(self, instance):
        if instance.order_set.count():
            raise ValidationError("Can not delete inventories with orders.")
        instance.delete()


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        inventories = (
            inventory.id
            for inventory in serializer.validated_data['inventories']
        )
        with transaction.atomic():
            Inventory.remove_from_inventory(inventories)
            serializer.save()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateOrderSerializer
        return OrderSerializer

    def perform_update(self, serializer):
        order = self.get_object()

        if order.status != Order.CREATED:
            raise ValidationError("Can't update finished or cancelled orders.")

        old_inventories = (inventory.id
                           for inventory in order.inventories.all())
        new_inventories = ()

        if serializer.validated_data['status'] != Order.CANCELLED:
            new_inventories = (
                inventory.id
                for inventory in serializer.validated_data['inventories']
            )

        with transaction.atomic():
            Inventory.add_to_inventory(old_inventories)
            Inventory.remove_from_inventory(new_inventories)
            serializer.save()

    def perform_destroy(self, instance):
        inventories = (inventory.id
                       for inventory in instance.inventories.all())
        with transaction.atomic():
            Inventory.add_to_inventory(inventories)
            instance.delete()
