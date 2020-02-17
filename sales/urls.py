from django.urls import path

from .views import InventoryListView, InventoryDetailView, OrderListView, \
    OrderDetailView

urlpatterns = [
    path('inventories/', InventoryListView.as_view(), name="inventory-list"),
    path('inventories/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
