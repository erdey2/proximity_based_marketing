from rest_framework import serializers
from advertisements.models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        # fields = ['advertisement_id', 'title', 'content', 'is_active', 'created_at', 'media_file']
        fields = '__all__'

class AdvertisementSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['title', 'content']