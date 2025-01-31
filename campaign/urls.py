from django.urls import path, include
from .api import advertisements_view, beacons_view, advertisements_log
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/beacons/', beacons_view.BeaconsList.as_view(), name='beacons_list'),
    path('api/beacons/<uuid:pk>', beacons_view.BeaconsDetail.as_view(), name='beacons_detail'),
    path('api/beacons/search', beacons_view.BeaconsSearch.as_view(), name='beacons_search'),
    path('api/beacons/active', beacons_view.BeaconsActive.as_view(), name='active_beacons'),
    path('api/beacons/count', beacons_view.BeaconsCount.as_view(),  name='count_beacons'),
    path('api/beacons/info', beacons_view.BeaconsInfo.as_view(), name='beacons_info'),

    path('api/advertisements/', advertisements_view.AdvertisementsList.as_view(), name='advertisements_list'),
    path('api/advertisements/<uuid:pk>', advertisements_view.AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('api/advertisements/active', advertisements_view.AdvertisementsActive.as_view(), name='advertisements_active'),
    path('api/advertisements/search', advertisements_view.AdvertisementsSearch.as_view(), name='advertisements_search'),


    # logs
    path('api/logs', advertisements_log.LogList.as_view(), name='logs_list'),
    path('api/logs/count', advertisements_log.LogsCount.as_view(), name='ads_count'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    #open api
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

]