from django.urls import path
from .views import (AdvertisementList, AdvertisementDetail, ViewAdListView, LikeAdView, ClickAdView,
                    SaveAdView, AdvertisementListWithPagination, AdInteractionView, LikedSavedAdsView,
                    AdvertisementDetailInteraction)
from assignments.views import AdvertisementBeaconsView

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details'),
    path('<uuid:pk>/interactions/', AdvertisementDetailInteraction.as_view(), name='advertisement-detail-interactions'),
    path('beacons/', AdvertisementBeaconsView.as_view(), name='advertisement-beacons'),
    path('pagination/', AdvertisementListWithPagination.as_view(), name='ads_paginated'),

    path('view-ad/', ViewAdListView.as_view(), name='view-ad'),
    path('like-ad/', LikeAdView.as_view(), name='like-ad'),
    path('click-ad/', ClickAdView.as_view(), name='click-ad'),
    path('save-ad/', SaveAdView.as_view(), name='save-ads'),
    path('interactions/', AdInteractionView.as_view(), name='ad-interactions'),
    path('like-save/', LikedSavedAdsView.as_view(), name='ad-like-save')

]
