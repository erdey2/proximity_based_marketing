from django.urls import path
from .views import AdvertisementAssignmentList, AdvertisementAssignmentDetail

urlpatterns = [
    path('', AdvertisementAssignmentList.as_view(), name='assignment_list'),
    path('<uuid:pk>/', AdvertisementAssignmentDetail.as_view(), name='assignment_details')
]
