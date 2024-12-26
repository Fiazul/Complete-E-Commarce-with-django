from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=2) and not self.is_email_verified


# Product Categories
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Products
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Product Variations (e.g., size, color)
class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations')
    variation_name = models.CharField(max_length=255)  # e.g., "Size", "Color"
    variation_value = models.CharField(max_length=255)  # e.g., "Large", "Red"

    def __str__(self):
        return f"{self.product.name} - {self.variation_name}: {self.variation_value}"


# Orders
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='orders')
    status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20, choices=status_choices, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_items')
    variation = models.ForeignKey(
        ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order {self.order.id}"


# Transactions
class Transaction(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='transaction')
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_method_choices = [
        ('Card', 'Card'),
        ('Paypal', 'Paypal'),
        ('Cash', 'Cash'),
    ]
    payment_method = models.CharField(
        max_length=20, choices=payment_method_choices)
    status_choices = [
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending'),
    ]
    status = models.CharField(
        max_length=20, choices=status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} for Order {self.order.id}"


# Dynamic Features Model for ML
class FeatureData(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return f"{self.key} for {self.product.name}"
