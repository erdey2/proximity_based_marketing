from django.urls import path
from .views import AdvertisementList, AdvertisementDetail

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<uuid:pk>/', AdvertisementDetail.as_view(), name='advertisement_details')
]
