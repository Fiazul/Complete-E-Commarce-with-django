from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusHistorySerializer
import uuid


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemCreateView(generics.CreateAPIView):
    """
    Handles adding items to an order.
    """
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        price = product.price
        order_id = self.kwargs['order_id']
        order = Order.objects.get(id=order_id, user=self.request.user)
        serializer.save(order=order, price=price)


class OrderStatusHistoryListView(generics.ListAPIView):
    """
    Handles listing status history for a specific order.
    """
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderStatusHistory.objects.filter(order__id=order_id, order__user=self.request.user)
