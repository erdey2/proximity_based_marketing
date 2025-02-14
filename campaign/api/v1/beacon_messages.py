from rest_framework import generics
from campaign.models import BeaconMessage
from campaign.serializers import BeaconMessageSerializer

class MessageCreate(generics.ListCreateAPIView):
    """Create and List messages from beacons"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer


class MessageDetail(generics.RetrieveDestroyAPIView):
    """"Get and delete messages"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer


