from rest_framework import serializers
from advertisements.models import Advertisement
from .models import AdView, AdLike, AdClick, AdSaved

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

class ViewAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True) # for input
    ad = AdvertisementSerializer(read_only=True)  # Nested serializer for ad details (output)
    viewed = serializers.BooleanField(default=True)

    class Meta:
        model = AdView
        fields = ['ad_id', 'ad', 'viewed', 'viewed_at']

    def create(self, validated_data):
        """Override create method to handle view action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Ensure `advertisement_id` is actually in the Advertisement model
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update ad click
        view, created = AdView.objects.get_or_create(user=user, ad=ad)
        view.viewed = True
        view.save()
        return view

class LikeAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Input only
    ad = AdvertisementSerializer(read_only=True)
    liked = serializers.BooleanField(default=True)

    class Meta:
        model = AdLike
        fields = ['ad_id', 'ad', 'liked', 'liked_at']

    def create(self, validated_data):
        """Override create method to handle like action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Ensure `advertisement_id` is actually in the Advertisement model
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update ad like
        like, created = AdLike.objects.get_or_create(user=user, ad=ad)
        like.liked = True
        like.save()
        return like

class ClickAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Input only
    ad = AdvertisementSerializer(read_only=True)
    clicked = serializers.BooleanField(default=True)

    class Meta:
        model = AdClick
        fields = ['ad_id', 'ad', 'clicked', 'clicked_at']

    def create(self, validated_data):
        """Override create method to handle click action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Ensure `advertisement_id` is actually in the Advertisement model
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update ad click
        click, created = AdClick.objects.get_or_create(user=user, ad=ad)
        click.clicked = True
        click.save()
        return click

class SaveAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Input only
    ad = AdvertisementSerializer(read_only=True)
    saved = serializers.BooleanField(default=True)

    class Meta:
        model = AdSaved
        fields = ['ad_id', 'ad', 'saved', 'saved_at']

    def create(self, validated_data):
        """Override create method to handle save action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Ensure `advertisement_id` is actually in the Advertisement model
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update ad click
        save, created = AdSaved.objects.get_or_create(user=user, ad=ad)
        save.saved = True
        save.save()
        return save

class AdInteractionSerializer(serializers.Serializer):
    ad = AdvertisementSerializer()  # Nested ad details
    viewed = serializers.BooleanField()
    viewed_at = serializers.DateTimeField(allow_null=True)
    liked = serializers.BooleanField()
    liked_at = serializers.DateTimeField(allow_null=True)
    clicked = serializers.BooleanField()
    clicked_at = serializers.DateTimeField(allow_null=True)
    saved = serializers.BooleanField()
    saved_at = serializers.DateTimeField(allow_null=True)
