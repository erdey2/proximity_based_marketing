from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from rest_framework.views import APIView
from campaign.models import Advertisement
from campaign.serializers import AdvertisementSerializer, AdvertisementWithBeaconsSerializer, AdvertisementSimpleSerializer, AdvertisementDateSerializer
from datetime import datetime
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class AdvertisementRateLimit(UserRateThrottle):
    rate = '1/minute'  # Custom throttle rate for this view

class AdvertisementList(ListCreateAPIView):
    """ List all advertisements or create a new one. """
    serializer_class = AdvertisementSerializer
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        qs = Advertisement.objects.all()
        title = self.request.GET.get('title')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if title:
            qs = qs.filter(title__icontains=title)
        if start_date:
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                qs = qs.filter(start_date__gte=parsed_start_date)
            except ValueError:
                return Advertisement.objects.none()  # Return empty queryset if date format is invalid

        if end_date:
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                qs = qs.filter(end_date__lte=parsed_end_date)
            except ValueError:
                return Advertisement.objects.none()
        return qs

    @extend_schema(
        summary="Retrieve Advertisements",
        description="""
            Retrieves a **paginated list** of advertisements with optional filters:

            **Filter Parameters:**
            - `title` (string, optional): Search for advertisements by title.
            - `start_date` (YYYY-MM-DD, optional): Filter ads that started **on or after** this date.
            - `end_date` (YYYY-MM-DD, optional): Filter ads that ended **on or before** this date.

            **Example Requests:**
            ```
            GET /api/advertisements/?title=Ybs soap &start_date=2024-01-01&end_date=2024-12-31
            ```

            **Responses:**
            - `200 OK`: Returns a paginated list of advertisements.
            - `400 Bad Request`: If an invalid date format is provided.
        """,
        parameters=[
            OpenApiParameter(name="title", type=str, description="Filter by advertisement title", required=False),
            OpenApiParameter(name="start_date", type=str, description="Filter by start date (YYYY-MM-DD)", required=False),
            OpenApiParameter(name="end_date", type=str, description="Filter by end date (YYYY-MM-DD)", required=False),
        ],
        responses={
            200: AdvertisementSerializer(many=True),
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Advertisement",
        description="""
            Creates a **new advertisement** with the required data.

            **Required Fields:**
            - `title` (string): The advertisement title.
            - `content` (string): The advertisement content
            - `start_date` (YYYY-MM-DD): The start date of the advertisement.
            - `end_date` (YYYY-MM-DD): The end date of the advertisement.

            **Example Request Body:**
            ```json
            {
                "title": "Gena Sale",
                "content": "We are offering a ybs soap with 30% discount", 
                "start_date": "2024-06-01",
                "end_date": "2024-06-30",
            }
            ```

            **Responses:**
            - `201 Created`: Successfully created a new advertisement.
            - `400 Bad Request`: If validation fails.
        """,
        request=AdvertisementSimpleSerializer,
        responses={
            201: AdvertisementSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an advertisement item."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()

    @extend_schema(
        summary="Retrieve an Advertisement",
        description="""
            Fetch the details of a specific advertisement using its `id`.

            **Example Request:**
            ```
            GET /api/advertisements/3/
            ```
            **Responses:**
            - `200 OK`: Returns advertisement details.
            - `404 Not Found`: If the advertisement does not exist.
        """,
        responses={
            200: AdvertisementSerializer,
            404: OpenApiResponse(description="Advertisement not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement",
        description="""
            Update an advertisement by replacing all its fields with new values.

            **Example Request Body:**
            ```json
            {
                "title": "Gena Sale",
                "content": "We are offering a ybs soap with 30% discount", 
                "start_date": "2025-12-01",
                "end_date": "2025-12-30",
            }
            ```
            **Responses:**
            - `200 OK`: Successfully updated the advertisement.
            - `400 Bad Request`: If validation fails.
            - `404 Not Found`: If the advertisement does not exist.
        """,
        request=AdvertisementSimpleSerializer,
        responses={
            200: AdvertisementSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Advertisement not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement",
        description="""
            Partially update an advertisement. Only the provided fields will be modified.

            **Example Request Body (Partial Update):**
            ```json
            {
                "end_date": "2025-05-26"
            }
            ```

            **Responses:**
            - `200 OK`: Successfully updated the advertisement.
            - `400 Bad Request`: If validation fails.
            - `404 Not Found`: If the advertisement does not exist.
        """,
        request=AdvertisementDateSerializer,
        responses={
            200: AdvertisementSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Advertisement not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an Advertisement",
        description="""
            Delete a specific advertisement using its `id`.

            **Example Request:**
            ```
            DELETE /api/advertisements/3/
            ```

            **Responses:**
            - `204 No Content`: Advertisement deleted successfully.
            - `404 Not Found`: If the advertisement does not exist.
        """,
        responses={
            204: OpenApiResponse(description="Advertisement deleted successfully"),
            404: OpenApiResponse(description="Advertisement not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AdvertisementActive(ListAPIView):
    """List all active advertisements."""
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        """Return only active advertisements based on start and end dates."""
        current_time = now()
        return Advertisement.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

    @extend_schema(
        summary="Get active advertisements",
        description="""
            Fetch all advertisements that are currently active based on their start and end dates.

            **Example Request:**
            ```
            GET /api/advertisements/active/
            ```

            **Responses:**
            - `200 OK`: Returns a list of active advertisements.
            - `404 Not Found`: If no active advertisements are available.
        """,
        responses={
            200: AdvertisementSerializer(many=True),
            404: OpenApiResponse(description="No active advertisements found")
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No active advertisements found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
