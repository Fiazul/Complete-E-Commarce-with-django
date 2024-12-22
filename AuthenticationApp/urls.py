from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, VerifyEmailView, RequestPasswordChangeView, VerifyOTPView, SetNewPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(),
         name='verify-email'),  # Verification URL
    path('request-password-change/', RequestPasswordChangeView.as_view(),
         name='request_password_change'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
