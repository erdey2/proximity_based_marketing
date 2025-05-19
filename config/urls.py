"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from dj_rest_auth.jwt_auth import get_refresh_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from core.campaign.views import api_root
from core.users.serializers import CustomLoginSerializer
from core.users.views import CustomLoginView

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', api_root, name='root_view'),
    path('api/v1/beacons/', include('core.beacons.urls')),  # Includes all beacon-related URLs
    path('api/v1/advertisements/', include('core.advertisements.urls')),
    path('api/v1/assignments/', include('core.assignments.urls')),
    path('api/v1/beacon-messages/', include('core.beacon_messages.urls')),
    path('api/v1/logs/', include('core.logs.urls')),
    path('api/v1/dashboards/', include('core.dashboards.urls')),

    # authentication & registration
    path('api/v1/auth/', include('dj_rest_auth.urls')),  # login, logout, password reset, etc.
    path("api/v1/auth/custom-login/", CustomLoginView.as_view(), name="custom-login"),
    path('api/v1/auth/password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')), # for social media login, registration
    path('api/v1/auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),

    # documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


