from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
import uuid


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'order', 'status', 'updated_at', 'note']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_email',
            'order_number',
            'created_at',
            'updated_at',
            'status',
            'total_price',
            'shipping_address',
            'billing_address',
            'items',
            'status_history',
        ]
        read_only_fields = ['user', 'order_number', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        order_number = str(uuid.uuid4()).replace('-', '').upper()[:20]
        validated_data['user'] = user
        validated_data['order_number'] = order_number
        order = Order.objects.create(**validated_data)
        return order
