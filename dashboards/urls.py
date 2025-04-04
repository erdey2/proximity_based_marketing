from django.urls import path
from .views import BeaconCount, BeaconLocationCount, BeaconMessageCountView, LogCount, PopularAdsView, ClicksPerDayAPIView, ImpressionsPerDayAPIView

urlpatterns = [
    path('count/', BeaconCount.as_view(), name='beacon_count'),
    path('location-count/', BeaconLocationCount.as_view(), name='location_count'),
    path('message-count/', BeaconMessageCountView.as_view(), name='message_count'),
    path('log-count/', LogCount.as_view(), name='log_count'),
    path('hot-ads/', PopularAdsView.as_view(), name='hot_ads'),
    path('clicks-per-day/', ClicksPerDayAPIView.as_view(), name='clicks-per-day'),
    path('impressions-per-day/', ImpressionsPerDayAPIView.as_view(), name='impressions-per-day')

]
