from django.urls import path
from .views import AdvertisementList, AdvertisementDetail, LikeAdView, SaveAdView, AdvertisementListWithPagination
from assignments.views import AdvertisementBeaconsView

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details'),
    path('beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons'),
    path('like-ad/', LikeAdView.as_view(), name='like-ad'),
    path('save/<uuid:pk>/', SaveAdView.as_view(), name='save-ads'),
    path('pagination/', AdvertisementListWithPagination.as_view(), name='ads_paginated')
]
