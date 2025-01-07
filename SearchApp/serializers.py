from rest_framework import serializers
from .models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'query', 'timestamp']
