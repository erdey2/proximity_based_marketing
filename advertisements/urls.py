from django.urls import path
from .views import AdvertisementList, AdvertisementDetail, ViewAdView, LikeAdView, ClickAdView, SaveAdView, AdvertisementListWithPagination
from assignments.views import AdvertisementBeaconsView

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details'),
    path('beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons'),
    path('pagination/', AdvertisementListWithPagination.as_view(), name='ads_paginated'),

    path('view-ad/', ViewAdView.as_view(), name='view-ad'),
    path('like-ad/', LikeAdView.as_view(), name='like-ad'),
    path('click-ad/', ClickAdView.as_view(), name='click-ad'),
    path('save-ad/', SaveAdView.as_view(), name='save-ads'),


]
