from rest_framework import serializers
from advertisements.models import Advertisement
from .models import AdEngagement

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        # fields = ['advertisement_id', 'title', 'content', 'is_active', 'created_at', 'media_file']
        fields = '__all__'

class AdvertisementSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'type', 'media_file']

class AdvertisementTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['title']

class LikeAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.IntegerField(write_only=True)  # Required for input

    class Meta:
        model = AdEngagement
        fields = ['ad_id', 'user', 'liked']


class SaveAdSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()