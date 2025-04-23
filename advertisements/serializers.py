from rest_framework import serializers
from advertisements.models import Advertisement
from .models import AdView, AdLike, AdClick, AdSaved
from django.utils.timezone import now

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

class AdvertisementDetailSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    liked_at = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    saved_at = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = [
            'advertisement_id', 'title', 'content', 'media_file', 'url', 'type', 'created_at',
            'liked', 'liked_at', 'saved', 'saved_at'
        ]

    def get_liked(self, ad):
        user = self.context['request'].user
        like = AdLike.objects.filter(ad=ad, user=user).first()
        return like.liked if like else False

    def get_liked_at(self, ad):
        user = self.context['request'].user
        like = AdLike.objects.filter(ad=ad, user=user).first()
        return like.liked_at if like else None

    def get_saved(self, ad):
        user = self.context['request'].user
        save = AdSaved.objects.filter(ad=ad, user=user).first()
        return save.saved if save else False

    def get_saved_at(self, ad):
        user = self.context['request'].user
        save = AdSaved.objects.filter(ad=ad, user=user).first()
        return save.saved_at if save else None

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
    ad_id = serializers.UUIDField(write_only=True)
    ad = AdvertisementSerializer(read_only=True)
    liked = serializers.BooleanField(default=True)

    class Meta:
        model = AdLike
        fields = ['ad_id', 'ad', 'liked', 'liked_at']

    def create(self, validated_data):
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        like, created = AdLike.objects.get_or_create(user=user, ad=ad)
        like.liked = True
        if not like.liked_at:
            like.liked_at = now()
        like.save()
        return like

class LikedAdDetailSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    liked_at = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    saved_at = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ['advertisement_id', 'title', 'content', 'type', 'url', 'media_file',
                  'created_at', 'is_active', 'liked', 'liked_at', 'saved', 'saved_at']

    def get_liked(self, ad):
        user = self.context['request'].user
        return AdLike.objects.filter(user=user, ad=ad, liked=True).exists()

    def get_liked_at(self, ad):
        user = self.context['request'].user
        like = AdLike.objects.filter(user=user, ad=ad, liked=True).first()
        return like.liked_at if like else None

    def get_saved(self, ad):
        user = self.context['request'].user
        return AdSaved.objects.filter(user=user, ad=ad, saved=True).exists()

    def get_saved_at(self, ad):
        user = self.context['request'].user
        save = AdSaved.objects.filter(user=user, ad=ad, saved=True).first()
        return save.saved_at if save else None

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
    ad_id = serializers.UUIDField(write_only=True)
    ad = AdvertisementSerializer(read_only=True)
    saved = serializers.BooleanField(default=True)

    class Meta:
        model = AdSaved
        fields = ['ad_id', 'ad', 'saved', 'saved_at']

    def create(self, validated_data):
        user = self.context['request'].user
        ad_id = validated_data.pop('ad_id')

        try:
            ad = Advertisement.objects.get(advertisement_id=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError({"ad_id": "Advertisement not found"})

        save, created = AdSaved.objects.get_or_create(user=user, ad=ad)
        save.saved = True
        if not save.saved_at:
            save.saved_at = now()
        save.save()
        return save

class SavedAdDetailSerializer(serializers.ModelSerializer):
    saved = serializers.SerializerMethodField()
    saved_at = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    liked_at = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ['advertisement_id', 'title', 'content', 'type', 'url', 'media_file',
                  'created_at', 'is_active', 'saved', 'saved_at', 'liked', 'liked_at']

    def get_saved(self, ad):
        user = self.context['request'].user
        return AdSaved.objects.filter(user=user, ad=ad, saved=True).exists()

    def get_saved_at(self, ad):
        user = self.context['request'].user
        save = AdSaved.objects.filter(user=user, ad=ad, saved=True).first()
        return save.saved_at if save else None

    def get_liked(self, ad):
        user = self.context['request'].user
        return AdLike.objects.filter(user=user, ad=ad, liked=True).exists()

    def get_liked_at(self, ad):
        user = self.context['request'].user
        like = AdLike.objects.filter(user=user, ad=ad, liked=True).first()
        return like.liked_at if like else None

class LikedSavedAdSerializer(serializers.Serializer):
    ad = AdvertisementSerializer()
    liked = serializers.BooleanField()
    liked_at = serializers.DateTimeField(allow_null=True)
    saved = serializers.BooleanField()
    saved_at = serializers.DateTimeField(allow_null=True)

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
