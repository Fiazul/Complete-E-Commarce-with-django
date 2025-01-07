from rest_framework import serializers
from .models import Category, UserCategoryPreference


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'description',
                  'is_active', 'created_at', 'updated_at', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data


class UserCategoryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategoryPreference
        fields = ['id', 'user', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']
