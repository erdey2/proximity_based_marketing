from django.urls import path
from .views import BeaconList, BeaconDetail, BeaconActive, BeaconLocationList, BeaconStatus, BeaconDataView
from assignments.views import BeaconAdvertisementsView

urlpatterns = [
    path('', BeaconList.as_view(), name='beacon-list'),
    path('<uuid:pk>/', BeaconDetail.as_view(), name='beacon-details'),
    path('active/', BeaconActive.as_view(), name='active-beacons'),
    path('location/', BeaconLocationList.as_view(), name='beacon-locations'),
    path('status/', BeaconStatus.as_view(), name='beacon-status'),
    path('advertisements/', BeaconAdvertisementsView.as_view(), name='beacon-ads'),
    path('data/<uuid:pk>/', BeaconDataView.as_view(), name='beacon-datav-iew')
]

