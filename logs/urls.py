from django.urls import path
from .views import LogList, LogDetail

urlpatterns = [
    path('logs/', LogList.as_view(), name='log_list'),
    path('logs/<uuid:pk>/', LogDetail.as_view(), name='log_details')
]