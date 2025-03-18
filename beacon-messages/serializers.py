from rest_framework import serializers
from beacon_messages.models import BeaconMessage

class BeaconMessageSerializer(serializers.ModelSerializer):
    beacon_name = serializers.CharField(source="beacon.name", read_only=True)

    class Meta:
        model = BeaconMessage
        fields = ['message_id', 'content', 'sent_at', 'read_at', 'beacon_id', 'beacon_name']

class BeaconMessageCountSerializer(serializers.Serializer):
    beacon_id = serializers.UUIDField(source="beacon__beacon_id")
    beacon_name = serializers.CharField(source="beacon__name")
    date = serializers.DateField()
    total_messages = serializers.IntegerField()