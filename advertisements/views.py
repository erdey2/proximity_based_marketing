from rest_framework.parsers import MultiPartParser, FormParser
from .models import Advertisement
from .serializers import AdvertisementSerializer, AdvertisementSimpleSerializer, AdvertisementTitleSerializer, LikeAdSerializer, SaveAdSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AdEngagement, SavedAd

class AdvertisementRateLimit(UserRateThrottle):
    rate = '100/minute'  # Custom throttle rate for this view

class AdvertisementPagination(PageNumberPagination):
    page_size = 3  # Default number of items per page
    page_query_param = 'page'  # Query parameter for specifying page number (e.g., ?page=2)
    page_size_query_param = 'page_size'  # Allows users to specify page size dynamically (e.g., ?page_size=10)
    max_page_size = 100  # Optional: Limit the maximum number of results per page

class AdvertisementList(ListCreateAPIView):
    """ List all advertisements or create a new one. """
    serializer_class = AdvertisementSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allows image uploads

    def get_queryset(self):
        qs = Advertisement.objects.all()
        title = self.request.GET.get('title')

        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    @extend_schema(
        tags=["Advertisements"],
        summary="Retrieve a list of advertisements",
        description="Fetch all advertisements. You can filter by the title by using the `title` query parameter.",
        parameters=[
            OpenApiParameter(name='title', type=str, required=False, description="Filter advertisements by title")
        ],
        responses={
            200: AdvertisementSerializer,
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Invalid parameters"}
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Advertisements"],
        summary="Create a new advertisement",
        description="Create a new advertisement by providing title, description, type and media_file.",
        request=AdvertisementSimpleSerializer,
        responses={
            201: AdvertisementSerializer,
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Invalid data. Please check the fields."}
                }
            }
        }

    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementListPagination(ListCreateAPIView):
    """List all advertisements or create a new one."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = AdvertisementPagination

    def get_queryset(self):
        qs = Advertisement.objects.all()
        title = self.request.GET.get('title')
        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    @extend_schema(
        tags=["Advertisements"],
        summary="List all Advertisements",
        description="Fetches a paginated list of advertisements. Supports filtering by title.",
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter advertisements by title (case insensitive).",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={200: AdvertisementSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Advertisements"],
        summary="Create an Advertisement",
        description="Creates a new advertisement with title, description, and image uploads.",
        request=AdvertisementSerializer,
        responses={201: AdvertisementSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an advertisement item."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        tags=["Advertisements"],
        summary="Retrieve an Advertisement",
        description="""
                Fetches a **single advertisement** by its ID.

                **Example Request:**
                ```
                GET /api/advertisements/1/
                ```

                **Responses:**
                - `200 OK`: Returns the advertisement details.
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
        tags=["Advertisements"],
        summary="Update an Advertisement",
        description="""
                Updates an **existing advertisement**.

                **Example Request Body:**
                ```json
                {
                    "title": "New Title",
                    "content": "Updated content."
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
        tags=["Advertisements"],
        summary="Partially Update an Advertisement",
        description="""
                Partially updates specific fields of an **existing advertisement**.

                **Example Request Body:**
                ```json
                {
                    "title": "Updated Title"
                }
                ```

                **Responses:**
                - `200 OK`: Successfully updated the advertisement.
                - `400 Bad Request`: If validation fails.
                - `404 Not Found`: If the advertisement does not exist.
            """,
        request=AdvertisementTitleSerializer,
        responses={
            200: AdvertisementSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Advertisement not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Advertisements"],
        summary="Delete an Advertisement",
        description="""
                Deletes an advertisement by its ID.

                **Example Request:**
                ```
                DELETE /api/advertisements/1/
                ```

                **Responses:**
                - `204 No Content`: Successfully deleted the advertisement.
                - `404 Not Found`: If the advertisement does not exist.
            """,
        responses={
            204: OpenApiResponse(description="Successfully deleted"),
            404: OpenApiResponse(description="Advertisement not found"),
        },

    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class LikeAdView(APIView):
    """Allow users to like an ad"""
    serializer_class = LikeAdSerializer

    @extend_schema(
        tags=['Advertisements'],
        summary="Like an Advertisement",
        description="Allows a user to like a specific advertisement.",
        request=LikeAdSerializer,
        parameters=[
            OpenApiParameter(
                name="ad_id",
                description="ID of the advertisement to like",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: {"description": "Ad liked successfully"},
            400: {"description": "Ad not found"},
        }

    )
    def post(self, request, ad_id):
        serializer = self.serializer_class(data={'ad_id': ad_id})
        if serializer.is_valid():
            try:
                ad = Advertisement.objects.get(id=ad_id)
                engagement, created = AdEngagement.objects.get_or_create(user=request.user, ad=ad)
                engagement.liked = True
                engagement.save()
                return Response({"message": "Ad liked successfully"})
            except Advertisement.DoesNotExist:
                return Response({"error": "Ad not found"}, status=400)
        return Response(serializer.errors, status=400)

class SaveAdView(APIView):
    """Allow users to save an ad for later"""
    serializer_class = SaveAdSerializer

    @extend_schema(
        tags=['Advertisements'],
        summary="Save an Advertisement",
        description="Allows a user to save an advertisement for later viewing.",
        request=SaveAdSerializer,
        parameters=[
            OpenApiParameter(
                name="ad_id",
                description="ID of the advertisement to save",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: {"message": "Ad saved successfully"},
            400: {"error": "Ad not found"}
        },

    )
    def post(self, request, ad_id):
        serializer = self.serializer_class(data={'ad_id': ad_id})
        if serializer.is_valid():
            try:
                ad = Advertisement.objects.get(id=ad_id)
                SavedAd.objects.create(user=request.user, ad=ad)
                return Response({"message": "Ad saved successfully"})
            except Advertisement.DoesNotExist:
                return Response({"error": "Ad not found"}, status=400)
        return Response(serializer.errors, status=400)





