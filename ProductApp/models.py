from django.db import migrations, models
import django.db.models.deletion
import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from CategoryApp.models import Category

User = get_user_model()


class Product(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE, default=1,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(
        upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure the media directory exists
        if self.product_image and not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        super(Product, self).save(*args, **kwargs)


class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations'
    )
    variation_name = models.CharField(max_length=255)  # e.g., "Size", "Color"
    variation_value = models.CharField(max_length=255)  # e.g., "Large", "Red"
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def __str__(self):
        return f"{self.product.name} - {self.variation_name}: {self.variation_value}"
