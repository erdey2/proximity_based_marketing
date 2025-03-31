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
    ad_id = serializers.UUIDField(write_only=True)  # Required for input
    viewed = serializers.BooleanField(default=True)

    class Meta:
        model = AdView
        fields = '__all__'

    def create(self, validated_data):
        """Override create method to handle the like action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Look up the ad by UUID
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update view
        view, created = AdLike.objects.get_or_create(user=user, ad=ad)
        view.viewed = validated_data.get('viewed', True)
        view.save()
        return view

class LikeAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Required for input
    liked = serializers.BooleanField(default=True)

    class Meta:
        model = AdLike
        fields = '__all__'

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
        like, created = AdLike.objects.get_or_create(user=user, ad=ad)
        like.liked = validated_data.get('liked', True)
        like.save()
        return like

class ClickAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Required for input
    clicked = serializers.BooleanField(default=True)

    class Meta:
        model = AdClick
        fields = '__all__'

    def create(self, validated_data):
        """Override create method to handle the click action"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Look up the ad by UUID
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Create or update click
        click, created = AdLike.objects.get_or_create(user=user, ad=ad)
        click.clicked = validated_data.get('clicked', True)
        click.save()
        return click

class SaveAdSerializer(serializers.ModelSerializer):
    ad_id = serializers.UUIDField(write_only=True)  # Required for input

    class Meta:
        model = AdSaved
        fields = '__all__'

    def create(self, validated_data):
        """Override create method to save an ad"""
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        # Look up the ad by UUID
        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        # Save the ad for the user
        saved_ad, created = AdSaved.objects.get_or_create(user=user, ad=ad)
        return saved_ad
