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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from campaign.views import api_root

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', api_root, name='root_view'),
    path('api/v1/beacons/', include('beacons.urls')),  # Includes all beacon-related URLs
    path('api/v1/advertisements/', include('advertisements.urls')),
    path('api/v1/assignments/', include('assignments.urls')),
    path('api/v1/beacon-messages/', include('beacon_messages.urls')),
    path('api/v1/logs/', include('logs.urls')),
    path('api/v1/dashboards/', include('dashboards.urls')),

    # user
    path('api/v1/users/', include('users.urls')),

    # documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # authentication & registration
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/auth/', include('dj_rest_auth.urls')),  # login, logout, password reset, etc.
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


