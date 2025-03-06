from campaign.models import Beacon, Advertisement, AdvertisementAssignment
from campaign.serializers import BeaconSerializer, BeaconListSerializer, AdvertisementAssignmentSerializer, AdvertisementWithBeaconsSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

class AdvertisementAssignmentPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 50

class AdvertisementAssignmentList(ListCreateAPIView):
    """API endpoint for listing and creating advertisement assignments."""

    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer
    pagination_class = AdvertisementAssignmentPagination

    @extend_schema(
        summary="List Advertisement Assignments",
        description="Retrieve a paginated list of all advertisement assignments.",
        responses={200: AdvertisementAssignmentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create an Advertisement Assignment",
        description="Create a new advertisement assignment by providing advertisement and beacon details.",
        request=AdvertisementAssignmentSerializer,
        responses={201: AdvertisementAssignmentSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementAssignmentDetail(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update, or delete an advertisement assignment by ID. """
    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer

    @extend_schema(
        summary="Retrieve an Advertisement Assignment",
        description="Get the details of a specific advertisement assignment by its ID.",
        responses={200: AdvertisementAssignmentSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement Assignment",
        description="Fully update an advertisement assignment by its ID.",
        request=AdvertisementAssignmentSerializer,
        responses={200: AdvertisementAssignmentSerializer}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement Assignment",
        description="Partially update specific fields of an advertisement assignment.",
        request=AdvertisementAssignmentSerializer,
        responses={200: AdvertisementAssignmentSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an Advertisement Assignment",
        description="Delete an advertisement assignment by its ID.",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AdvertisementListWithBeaconsView(ListAPIView):
    """ API endpoint to list advertisements along with their assigned beacons. """
    queryset = Advertisement.objects.prefetch_related("advertisement_assignments__beacon").all()
    serializer_class = AdvertisementWithBeaconsSerializer
    pagination_class = AdvertisementAssignmentPagination

    @extend_schema(
        summary="List Advertisements with Beacons",
        description="Retrieve a list of advertisements along with the beacons they are assigned to.",
        responses={200: AdvertisementWithBeaconsSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BeaconListWithAdsView(ListAPIView):
    """ API endpoint to list beacons along with their assigned advertisements."""
    queryset = Beacon.objects.prefetch_related("advertisement_assignments__advertisement").all()
    serializer_class = BeaconListSerializer
    pagination_class = AdvertisementAssignmentPagination

    @extend_schema(
        summary="List Beacons with Advertisements",
        description="Retrieve a list of beacons along with the advertisements they have been assigned.",
        responses={200: BeaconSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
