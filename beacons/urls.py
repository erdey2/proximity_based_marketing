from django.urls import path
from .views import BeaconList, BeaconDetail, BeaconLocationList, BeaconStatus

urlpatterns = [
    path('', BeaconList.as_view(), name='beacon_list'),
    path('<uuid:pk>/', BeaconDetail.as_view(), name='beacon_details'),
    path('beacons-location/', BeaconLocationList.as_view(), name='beacon_locations'),
    path('beacons-status/', BeaconStatus.as_view(), name='beacon_status')
]

