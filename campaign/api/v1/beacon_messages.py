from rest_framework.generics import ListCreateAPIView
from campaign.models import BeaconMessage
from campaign.serializers import BeaconMessageSerializer

class CreateMessages(ListCreateAPIView):
    """Create and List messages from beacons"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer

