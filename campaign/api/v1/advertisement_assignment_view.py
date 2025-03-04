from campaign.models import Beacon, Advertisement, AdvertisementAssignment
from campaign.serializers import BeaconSerializer, AdvertisementAssignmentSerializer, AdvertisementWithBeaconsSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination


class AdvertisementAssignmentPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 50

class AdvertisementAssignmentList(ListCreateAPIView):
    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer
    pagination_class = AdvertisementAssignmentPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AdvertisementAssignmentDetail(RetrieveUpdateDestroyAPIView):
    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer

class AdvertisementListWithBeaconsView(ListAPIView):
    queryset = Advertisement.objects.prefetch_related("advertisement_assignments__beacon").all()
    serializer_class = AdvertisementWithBeaconsSerializer
    pagination_class = AdvertisementAssignmentPagination

class BeaconListWithAdsView(ListAPIView):
    queryset = Beacon.objects.prefetch_related("advertisement_assignments__advertisement").all()
    serializer_class = BeaconSerializer
    pagination_class = AdvertisementAssignmentPagination
