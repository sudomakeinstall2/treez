from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .serializers import InventorySerializer, OrderSerializer
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