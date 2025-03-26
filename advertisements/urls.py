from django.urls import path
from .views import AdvertisementList, AdvertisementDetail, LikeAdView, SaveAdView, AdvertisementListPagination
from assignments.views import AdvertisementBeaconsView

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details'),
    path('beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons'),
    path('like/<uuid:pk>/', LikeAdView.as_view(), name='like-ads'),
    path('save/<uuid:pk>/', SaveAdView.as_view(), name='save-ads'),
    path('pagination', AdvertisementListPagination.as_view(), name='ads_paginated')
]
