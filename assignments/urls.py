from django.urls import path
from .views import AdvertisementAssignmentList, AdvertisementAssignmentDetail, AdvertisementActive, AdvertisementBeaconsView, BeaconAdvertisementsView

urlpatterns = [
    path('', AdvertisementAssignmentList.as_view(), name='assignment_list'),
    path('<uuid:pk>/', AdvertisementAssignmentDetail.as_view(), name='assignment_details'),
    path('active/', AdvertisementActive.as_view(), name='active_advertisements'),

]
