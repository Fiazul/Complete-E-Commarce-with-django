from rest_framework import serializers
from .models import Product, ProductVariation
from django.contrib.auth import get_user_model
from CategoryApp.models import Category
User = get_user_model()


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'variation_name',
                  'variation_value', 'additional_price']


class ProductSerializer(serializers.ModelSerializer):
    variations = ProductVariationSerializer(many=True, read_only=True)
    product_image = serializers.ImageField(
        required=False)  # Ensure image is handled correctly
    user = serializers.ReadOnlyField(source='User.username')
    category = serializers.CharField(
        write_only=True)
    category_id = serializers.StringRelatedField(
        read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'user', 'name', 'description', 'price', 'stock', 'is_active',
            'category', 'category_id', 'created_at', 'updated_at', 'product_image', 'variations'
        ]
        read_only_fields = ['user', 'category_id']

    def create(self, validated_data):
        image = validated_data.pop('product_image', None)
        category = validated_data.pop('category')
        category_id, created = Category.objects.get_or_create(name=category)
        validated_data['category'] = category_id

        product = Product.objects.create(**validated_data)

        if image:
            product.product_image = image
            product.save()

        return product

    def update(self, instance, validated_data):
        # Handle file upload manually for updates
        image = validated_data.pop('product_image', None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)

        if image:
            instance.product_image = image

        instance.save()
        return instance
