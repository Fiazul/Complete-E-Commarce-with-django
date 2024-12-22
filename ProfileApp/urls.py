from django.urls import path
from .views import ProfileView, UpdateSellerStatusView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update-seller-status/', UpdateSellerStatusView.as_view(),
         name='update-seller-status'),
]
