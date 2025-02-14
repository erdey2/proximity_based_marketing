from rest_framework import generics
from campaign.models import BeaconMessage
from campaign.serializers import BeaconMessageSerializer
from drf_spectacular.utils import extend_schema

class MessageCreate(generics.ListCreateAPIView):
    """Create and List messages from beacons"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer

    @extend_schema(
        tags=['Messages'],
        summary="List all messages sent by beacons",
        description="Retrieve a list of all existing messages.",
        responses={200: BeaconMessageSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Messages'],
        summary="Create a new message",
        description="Create a new message with the provided data.",
        request=BeaconMessageSerializer,
        responses={201: BeaconMessageSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MessageDetail(generics.RetrieveDestroyAPIView):
    """Get and delete messages"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer

    @extend_schema(
        tags=['Messages'],
        summary="Retrieve a specific Beacon Message",
        description="Retrieve a Beacon Message by its ID.",
        responses={200: BeaconMessageSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Messages'],
        summary="Delete a specific Beacon Message",
        description="Delete a Beacon Message by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
