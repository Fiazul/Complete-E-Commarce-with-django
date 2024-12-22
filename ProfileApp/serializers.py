from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_seller', 'bio', 'phone', 'address',
                  'profile_picture', 'date_of_birth', 'website']


class UpdateSellerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_seller']
