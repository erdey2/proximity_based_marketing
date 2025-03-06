from django.urls import path
from .api.v1 import advertisement_view, beacon_view, log_view, advertisement_assignment_view, message_view, root_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    # root
    path('', root_view.api_root, name='root'),

    # beacon related views
    path('api/v1/beacons/', beacon_view.BeaconList.as_view(), name='beacons_list'),
    path('api/v1/beacons/<uuid:pk>/', beacon_view.BeaconDetail.as_view(), name='beacons_detail'),
    path('api/v1/beacons/active/', beacon_view.BeaconActive.as_view(), name='active_beacons'),
    path('api/v1/beacons/count/', beacon_view.BeaconCount.as_view(), name='count_beacons'),
    path('api/v1/beacons/locations_count/', beacon_view.BeaconLocationCount.as_view(), name='total_locations'),
    path('api/v1/beacons/status/<uuid:pk>/', beacon_view.BeaconStatus.as_view(), name='check_beacon_status'),

    # advertisement related views
    path('api/v1/advertisements/', advertisement_view.AdvertisementList.as_view(), name='advertisements_list'),
    path('api/v1/advertisements/<uuid:pk>/', advertisement_view.AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('api/v1/advertisements/cached/', advertisement_view.CachedAdvertisementList.as_view(), name='cached_ad'),
    path('api/v1/advertisements/active/', advertisement_view.AdvertisementActive.as_view(), name='advertisements_active'),

    # advertisement assignments
    path('api/v1/advertisements/assignments/', advertisement_assignment_view.AdvertisementAssignmentList.as_view(), name='advertisement_assignment'),
    path('api/v1/advertisements/assignments/<uuid:pk>/', advertisement_assignment_view.AdvertisementAssignmentDetail.as_view(), name='advertisement_assignment_detail'),
    path('api/v1/beacons/advertisements/', advertisement_assignment_view.BeaconListWithAdsView.as_view(), name='beacons_ads'),
    path('api/v1/advertisements/beacons/', advertisement_assignment_view.AdvertisementListWithBeaconsView.as_view(), name='advertisements_beacons'),

    # logs
    path('api/v1/logs/', log_view.LogList.as_view(), name='logs_list'),
    path('api/v1/logs/<int:pk>/', log_view.LogDetail.as_view(), name='logs_detail'),
    path('api/v1/logs/count/', log_view.LogCount.as_view(), name='ads_count'),

    # view for messages sent from beacons
    path('api/v1/messages/', message_view.MessageList.as_view(), name='message_create'),
    path('api/v1/messages/<uuid:pk>/', message_view.MessageDetail.as_view(), name='message_detail'),
    path('api/v1/beacons/messages/count/', message_view.BeaconMessageCountView.as_view(), name='beacon_messages_count'),

    # documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # authentication
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]