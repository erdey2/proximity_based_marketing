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
    ad_id = serializers.UUIDField(write_only=True)  # Required for input
    liked = serializers.BooleanField(default=True)

    class Meta:
        model = AdEngagement
        fields = ['ad_id', 'liked']

    def create(self, validated_data):
        """Override create method to handle the like action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Look up the ad by UUID
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update engagement
        engagement, created = AdEngagement.objects.get_or_create(user=user, ad=ad)
        engagement.liked = validated_data.get('liked', True)
        engagement.save()

        return engagement

class SaveAdSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()