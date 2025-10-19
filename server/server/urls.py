from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from django.urls import (
    path,
    include
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'nested_admin/',
        include('nested_admin.urls')
    ),
    path(
        'i18n/',
        include('django.conf.urls.i18n')
    ),

    # JWT
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Schema & Docs
    path(
        'api/schema/',
        SpectacularAPIView.as_view(
            permission_classes=[permissions.AllowAny]
        ),
        name='schema'
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[permissions.AllowAny]
        ),
        name='swagger-ui'
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
