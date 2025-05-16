from django.urls import path
from .views import LogList, LogDetail

urlpatterns = [
    path('', LogList.as_view(), name='log_list'),
    path('<uuid:pk>/', LogDetail.as_view(), name='log_details')
]