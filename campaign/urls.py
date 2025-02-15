from django.urls import path
from .api.v1 import advertisement_view, beacon_view, advertisement_log
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .api.v1.message_view import MessageCreate, MessageDetail


urlpatterns = [
    # beacon related views
    path('api/v1/beacons/', beacon_view.BeaconList.as_view(), name='beacons_list'),
    path('api/v1/beacons/<uuid:pk>', beacon_view.BeaconDetail.as_view(), name='beacons_detail'),
    path('api/v1/beacons/search', beacon_view.BeaconsSearch.as_view(), name='beacons_search'),
    path('api/v1/beacons/active', beacon_view.BeaconActive.as_view(), name='active_beacons'),
    path('api/v1/beacons/count', beacon_view.BeaconCount.as_view(), name='count_beacons'),
    path('api/v1/beacons/locations_count', beacon_view.BeaconLocationCount.as_view(), name='total_locations'),
    path('api/v1/beacons/beacons_info_update', beacon_view.BeaconInfoUpdate.as_view(), name='beacons_info'),
    path('api/v1/beacons/status/<uuid:pk>', beacon_view.BeaconStatus.as_view(), name='check_beacon_status'),

    # advertisement related views
    path('api/v1/advertisements/', advertisement_view.AdvertisementsList.as_view(), name='advertisements_list'),
    path('api/v1/advertisements/<uuid:pk>', advertisement_view.AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('api/v1/advertisements/active', advertisement_view.AdvertisementsActive.as_view(), name='advertisements_active'),
    path('api/v1/advertisements/search', advertisement_view.AdvertisementsSearch.as_view(), name='advertisements_search'),

    # logs
    path('api/v1/logs', advertisement_log.LogList.as_view(), name='logs_list'),
    path('api/v1/logs/count', advertisement_log.LogsCount.as_view(), name='ads_count'),

    # view for messages sent from beacons
    path('api/v1/messages', MessageCreate.as_view(), name='message_create'),
    path('api/v1/messages/<uuid:pk>', MessageDetail.as_view(), name='message_detail'),

    # documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # authentication
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]