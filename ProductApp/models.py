from django.db import migrations, models
import django.db.models.deletion
import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
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


User = get_user_model()


def set_default_seller_user(apps, schema_editor):
    Product = apps.get_model('ProductApp', 'Product')
    default_user = User.objects.first()
    for product in Product.objects.all():
        product.seller_user = default_user
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_user',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to=User),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_seller_user),
    ]
