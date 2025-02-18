from campaign.models import Advertisement
from campaign.serializers import AdvertisementSerializer
from rest_framework import status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter


class AdvertisementRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Custom throttle rate for this view

class AdvertisementPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 50

class AdvertisementsList(ListCreateAPIView):
    #@throttle_classes([AdvertisementRateThrottle, AnonRateThrottle])
    """ List all advertisements or create a new one. """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    # search advertisement by title, start_date etc
    """ filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'type'] """

    def get_queryset(self):
        qs = Advertisement.objects.all()
        title = self.request.GET.get('title')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        is_active = self.request.GET.get('is_active')
        type = self.request.GET.get('type')

        if title:
            qs = qs.filter(title__icontains=title)
            return qs
        if start_date:
            qs = qs.filter(start_date__contains=start_date)
            return qs
        if end_date:
            qs = qs.filter(end_date__icontains=end_date)
            return qs
        if is_active:
            qs = qs.filter(is_active__icontains=is_active)
            return qs
        if type:
            qs = qs.filter(type__icontains=type)
            return qs

    @extend_schema(
        summary="Retrieve Advertisements",
        description="Retrieve a paginated list of all advertisements.",
        responses={200: AdvertisementSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Advertisement",
        description="Create a new advertisement with the provided data.",
        request=AdvertisementSerializer,
        responses={
            201: AdvertisementSerializer,
            400: {"message": "Invalid input data."},
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdvertisementDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an advertisement item."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    @extend_schema(
        summary="Retrieve an Advertisement",
        description="Fetch details of a specific advertisement by its ID.",
        responses={200: AdvertisementSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement",
        description="Update an advertisement's details with the provided data.",
        request=AdvertisementSerializer,
        responses={
            200: AdvertisementSerializer,
            400: {"message": "Invalid input data."},
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement",
        description="Partially update an advertisement using only the provided fields.",
        request=AdvertisementSerializer,
        responses={
            200: AdvertisementSerializer,
            400: {"message": "Invalid input data."},
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an Advertisement",
        description="Delete a specific advertisement by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AdvertisementsActive(ListAPIView):
    """List all active advertisements."""
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        """Return only active advertisements based on start and end dates."""
        current_time = now()
        return Advertisement.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

    @extend_schema(
        summary="Get active advertisements",
        description="Fetch all advertisements that are currently active based on their start and end dates.",
        responses={200: AdvertisementSerializer(many=True), 404: {"message": "No active advertisements found."}}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No active advertisements found."}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)
