from django.urls import path
from .views import AdvertisementAssignmentList, AdvertisementAssignmentDetail, AdvertisementActive, AdvertisementBeaconsView, BeaconAdvertisementsView

urlpatterns = [
    path('', AdvertisementAssignmentList.as_view(), name='assignment_list'),
    path('<uuid:pk>/', AdvertisementAssignmentDetail.as_view(), name='assignment_details'),
    path('active/', AdvertisementActive.as_view(), name='active_advertisements'),
    path('beacon-advertisements/', BeaconAdvertisementsView.as_view(), name='beacon-ads'),
    path('advertisement-beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons')

]
