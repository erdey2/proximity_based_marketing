from django.urls import path
from .views import AdvertisementList, AdvertisementDetail
from assignments.views import AdvertisementBeaconsView

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details'),
    path('beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons')
]
