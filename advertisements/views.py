from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Advertisement
from .serializers import AdvertisementSerializer, AdvertisementSimpleSerializer, AdvertisementTitleSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.response import Response
from .models import AdView, AdLike, AdClick, AdSaved
from .serializers import ViewAdSerializer, LikeAdSerializer, ClickAdSerializer, SaveAdSerializer

class AdvertisementRateLimit(UserRateThrottle):
    rate = '100/minute'  # Custom throttle rate for this view

class AdvertisementPagination(PageNumberPagination):
    page_size = 3  # Default number of items per page
    page_query_param = 'page'  # Query parameter for specifying page number (e.g., ?page=2)
    page_size_query_param = 'page_size'  # Allows users to specify page size dynamically (e.g., ?page_size=10)
    max_page_size = 100  # Optional: Limit the maximum number of results per page
    invalid_page_message = '[]'

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

class AdvertisementListWithPagination(ListCreateAPIView):
    """List all advertisements or create a new one."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all().order_by('created_at')
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

class ViewAdView(ListCreateAPIView):
    """Allow users to view an ad and retrieve their viewed ads"""
    serializer_class = ViewAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the viewed ads of the authenticated user"""
        return AdView.objects.filter(user=self.request.user)

    @extend_schema(
        tags=["Advertisements"],
        summary="Retrieve user's viewed ads",
        description="Returns a list of ads that the authenticated user has viewed.",
        responses={200: ViewAdSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="View an Advertisement",
        description="Allows a user to view an advertisement by providing `ad_id` in the request body.",
        request=ViewAdSerializer,
        responses={
            201: {"description": "Ad viewed successfully"},
            400: {"description": "Invalid request"},
            404: {"description": "Advertisement not found"},
        },
    )
    def post(self, request, *args, **kwargs):
        """Allow users to view an ad"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad view successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeAdView(ListCreateAPIView):
    """Allow users to like an ad and retrieve their liked ads"""
    serializer_class = LikeAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the liked ads of the authenticated user"""
        return AdLike.objects.filter(user=self.request.user)

    @extend_schema(
        tags=['Advertisements'],
        summary="Retrieve user's liked ads",
        description="Returns a list of ads that the authenticated user has liked.",
        responses={200: LikeAdSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Like an Advertisement",
        description="Allows a user to like an advertisement by providing `ad_id` in the request body.",
        request=LikeAdSerializer,
        responses={
            201: {"description": "Ad liked successfully"},
            400: {"description": "Invalid request"},
            404: {"description": "Advertisement not found"},
        },
    )
    def post(self, request, *args, **kwargs):
        """Allow users to like an ad"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad liked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClickAdView(ListCreateAPIView):
    """View for tracking ad clicks"""
    serializer_class = ClickAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the liked ads of the authenticated user"""
        return AdClick.objects.filter(user=self.request.user)

    @extend_schema(
        tags=['Advertisements'],
        summary="Retrieve Clicked Ads",
        description="Returns a list of all ads that the authenticated user has clicked.",
        responses={200: ClickAdSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Click an Advertisement",
        description="Allows a user to record a click on an advertisement. The request should include the advertisement ID.",
        request=ClickAdSerializer,
        responses={
            201: {"description": "Ad clicked successfully"},
            400: {"description": "Invalid request"},
        },
        parameters=[
            OpenApiParameter(
                name="ad_id",
                description="UUID of the advertisement being clicked",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """Allow users to click an ad"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad clicked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaveAdView(ListCreateAPIView):
    """Allow users to save an ad for later"""
    serializer_class = SaveAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the liked ads of the authenticated user"""
        return AdSaved.objects.filter(user=self.request.user)

    @extend_schema(
        tags=['Advertisements'],
        summary="Retrieve Saved Ads",
        description="Returns a list of all ads that the authenticated user has saved.",
        responses={200: SaveAdSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Save an Advertisement",
        description="Allows a user to record a save on an advertisement. The request should include the advertisement ID.",
        request=SaveAdSerializer,
        responses={
            201: {"description": "Ad saved successfully"},
            400: {"description": "Invalid request"},
        },
        parameters=[
            OpenApiParameter(
                name="ad_id",
                description="UUID of the advertisement being saved",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """Allow users to click an ad"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad saved successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





