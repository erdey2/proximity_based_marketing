from django.urls import path, include
from .api import advertisements_view, beacons_view, advertisements_log
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from campaign import scan_check
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/beacons/', beacons_view.beacons_list, name='beacons_list'),
    path('api/beacons/<uuid:uuid>', beacons_view.beacons_detail, name='beacons_detail'),
    path('api/beacons/search', beacons_view.beacons_search, name='beacons_search'),
    path('api/beacons/active', beacons_view.active_beacons, name='active_beacons'),
    path('api/beacons/count', beacons_view.beacons_count,  name='count_beacons'),

    # path('api/beacons', beacons_view.AllBeacons.as_view(), name='all_beacons'),
    path('api/beacons/info', beacons_view.beacons_info, name='beacons_info'),

    path('api/advertisements/', advertisements_view.advertisements_list, name='advertisement_list'),
    path('api/advertisements/<uuid:uuid>', advertisements_view.advertisements_detail, name='advertisement_detail'),
    path('api/advertisements/active', advertisements_view.advertisements_active, name='advertisements_active'),
    path('api/advertisements/search', advertisements_view.advertisements_search, name='advertisements_search'),


    # logs
    path('api/logs', advertisements_log.log_list, name='logs_list'),
    path('api/logs/count', advertisements_log.log_count, name='ads_count'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('home/', scan_check.scan_beacons, name='scan_check'),


    #open api
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),



]