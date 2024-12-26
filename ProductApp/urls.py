from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductVariationListCreateView,
    ProductVariationDetailView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/variations/',
         ProductVariationListCreateView.as_view(), name='product-variation-list-create'),
    path('product-variations/<int:pk>/',
         ProductVariationDetailView.as_view(), name='product-variation-detail'),
]
