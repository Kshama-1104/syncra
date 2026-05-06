from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Profile
from common.services.email import send_transactional_email
from .serializers import (
    EmailSerializer,
    GoogleLoginSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    ProfileSerializer,
    RegisterSerializer,
    TokenConfirmSerializer,
    UserSerializer,
    token_pair_for_user,
)

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        if self.action in {"forgot_password", "request_email_verification"}:
            return EmailSerializer
        if self.action == "verify_email":
            return TokenConfirmSerializer
        if self.action == "reset_password":
            return PasswordResetConfirmSerializer
        if self.action == "google":
            return GoogleLoginSerializer
        return LoginSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user).data, "tokens": token_pair_for_user(user)}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"user": UserSerializer(user).data, "tokens": token_pair_for_user(user)})

    @action(detail=False, methods=["post"])
    def forgot_password(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            token = default_token_generator.make_token(user)
            send_transactional_email("Reset your Syncra password", f"Use token {token} for user id {user.id}.", user.email)
        return Response({"detail": "If the email exists, a reset link has been sent."})

    @action(detail=False, methods=["post"])
    def request_email_verification(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            token = default_token_generator.make_token(user)
            send_transactional_email("Verify your Syncra email", f"Use token {token} for user id {user.id}.", user.email)
        return Response({"detail": "If the email exists, a verification link has been sent."})

    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(id=serializer.validated_data["uid"]).first()
        if not user or not default_token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Invalid or expired reset token."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Password updated successfully."})

    @action(detail=False, methods=["post"])
    def verify_email(self, request):
        serializer = TokenConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(id=serializer.validated_data["uid"]).first()
        if not user or not default_token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Invalid or expired verification token."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])
        return Response({"detail": "Email verified."})

    @action(detail=False, methods=["post"], url_path="google")
    def google(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"detail": "Install google-auth and verify the Google ID token here before issuing Syncra JWTs."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user=self.request.user)


class UserSearchView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username", "email", "profile__display_name"]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id).select_related("profile").only("id", "username", "email", "avatar", "is_email_verified")
