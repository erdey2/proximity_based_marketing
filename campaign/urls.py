from django.urls import path
from .api.v1 import advertisements_view, beacons_view, advertisements_log
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/v1/beacons/', beacons_view.BeaconsList.as_view(), name='beacons_list'),
    path('api/v1/beacons/<uuid:pk>', beacons_view.BeaconsDetail.as_view(), name='beacons_detail'),
    path('api/v1/beacons/search', beacons_view.BeaconsSearch.as_view(), name='beacons_search'),
    path('api/v1/beacons/active', beacons_view.BeaconsActive.as_view(), name='active_beacons'),
    path('api/v1/beacons/count', beacons_view.BeaconsCount.as_view(), name='count_beacons'),
    path('api/v1/beacons/locations_count', beacons_view.BeaconsLocationsCount.as_view(), name='total_locations'),
    path('api/v1/beacons/beacons_info_update', beacons_view.BeaconsInfoUpdate.as_view(), name='beacons_info'),
    path('api/v1/beacons/status/<uuid:pk>', beacons_view.BeaconsStatus.as_view(), name='check_beacon_status'),

    path('api/v1/advertisements/', advertisements_view.AdvertisementsList.as_view(), name='advertisements_list'),
    path('api/v1/advertisements/<uuid:pk>', advertisements_view.AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('api/v1/advertisements/active', advertisements_view.AdvertisementsActive.as_view(), name='advertisements_active'),
    path('api/v1/advertisements/search', advertisements_view.AdvertisementsSearch.as_view(), name='advertisements_search'),


    # logs
    path('api/v1/logs', advertisements_log.LogList.as_view(), name='logs_list'),
    path('api/v1/logs/count', advertisements_log.LogsCount.as_view(), name='ads_count'),


    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    #open api
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]