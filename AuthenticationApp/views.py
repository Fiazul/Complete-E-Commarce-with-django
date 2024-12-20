from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer
from django.core.mail import EmailMessage
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, SetNewPasswordSerializer, VerifyOTPSerializer, RequestPasswordChangeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import OTP
import random
User = get_user_model()


def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt="email-verification-salt")


def verify_verification_token(token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt="email-verification-salt", max_age=3600  # 1 hour
        )
        return email
    except Exception:
        return None


def send_verification_email(user, token):
    verification_link = f"http://127.0.0.1:8000/auth/verify-email/?token={token}"
    email_subject = "Verify Your Email Address"
    email_body = f"""
    Hi {user.username},

    Please verify your email by clicking the link below:
    {verification_link}

    If you didn't register, you can ignore this email.
    """
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()


# Views
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_verification_token(user.email)
            send_verification_email(user, token)
            return Response(
                {"message": "User registered successfully! Please verify your email."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({"error": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()  # Blacklist token
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        email = verify_verification_token(token)
        if email:
            try:
                user = User.objects.get(email=email)
                if user.is_verified:
                    return Response({"message": "Email already verified!"}, status=status.HTTP_200_OK)
                user.is_verified = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordChangeView(APIView):
    def post(self, request):
        serializer = RequestPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            otp_code = otp = str(random.randint(100000, 999999))

            # Generate and save OTP
            # Replace with random OTP logic
            otp = OTP.objects.create(user=user, code=otp_code)

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {otp.code}. It expires in 2 minutes.',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']

            user = User.objects.filter(email=email).first()
            otp_entry = OTP.objects.filter(user=user, code=otp_code).first()

            if not otp_entry or not otp_entry.is_valid():
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

            otp_entry.is_email_verified = True
            otp_entry.save()

            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            user = User.objects.get(email=email)

            otp_entry = OTP.objects.filter(user=user).last()
            if not otp_entry or not otp_entry.is_email_verified:
                return Response({"error": "Please verify your email before changing the password."}, status=status.HTTP_403_FORBIDDEN)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
