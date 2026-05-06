from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import AuthViewSet, ProfileViewSet, UserSearchView
from apps.chats.views import ChatViewSet, MessageViewSet
from apps.mediafiles.views import MediaAssetViewSet
from apps.notifications.views import NotificationViewSet

router = DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("chats", ChatViewSet, basename="chats")
router.register("messages", MessageViewSet, basename="messages")
router.register("media", MediaAssetViewSet, basename="media")
router.register("notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/users/search/", UserSearchView.as_view(), name="user-search"),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
