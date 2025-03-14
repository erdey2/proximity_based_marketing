from campaign.models import Advertisement
from campaign.serializers import AdvertisementSerializer, AdvertisementSimpleSerializer, AdvertisementDateSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class AdvertisementRateLimit(UserRateThrottle):
    rate = '100/minute'  # Custom throttle rate for this view

class AdvertisementList(ListCreateAPIView):
    """ List all advertisements or create a new one. """
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        qs = Advertisement.objects.all()
        title = self.request.GET.get('title')

        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    @extend_schema(
        summary="Retrieve Advertisements",
        description="""
            Retrieves a **paginated list** of advertisements with optional filters:

            **Filter Parameters:**
            - `title` (string, optional): Search for advertisements by title.

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

            **Example Request Body:**
            ```json
            {
                "title": "Gena Sale",
                "content": "We are offering a ybs soap with 30% discount", 
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
