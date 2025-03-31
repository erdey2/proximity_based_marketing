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
    serializer_class = ViewAdSerializer
    queryset = AdView.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Advertisements'],
        summary="List all ad views",
        description="Retrieves a list of all recorded ad views. Requires authentication.",
        responses={200: ViewAdSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Create a new ad view",
        description="Logs a new ad view when a user views an advertisement.",
        request=ViewAdSerializer,
        responses={201: ViewAdSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(self, *args, **kwargs)

class LikeAdView(ListCreateAPIView):
    """Allow users to like an ad and retrieve all liked ads"""
    serializer_class = LikeAdSerializer
    queryset = AdLike.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Advertisements'],
        summary="Retrieve all liked ads",
        description="Returns a list of all ad engagements (likes) by authenticated users.",
        responses={200: LikeAdSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Like an Advertisement",
        description="Allows a user to like an advertisement using UUID.",
        request=LikeAdSerializer,  # Define the expected request body
        responses={
            201: {"description": "Ad liked successfully"},
            400: {"description": "Invalid request"},
            404: {"description": "Advertisement not found"},
        },
        parameters=[
            OpenApiParameter(
                name="ad_id",
                description="UUID of the advertisement to like",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """Allow users to like an ad"""
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad liked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClickAdView(ListCreateAPIView):
    serializer_class = ClickAdSerializer
    queryset = AdClick.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Advertisements'],
        summary="List all ad clicks",
        description="Retrieves a list of all recorded ad clicks. Requires authentication.",
        responses={200: ClickAdSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Create a new ad click",
        description="Logs a new ad click when a user clicks on an advertisement.",
        request=ClickAdSerializer,
        responses={201: ClickAdSerializer}
    )
    def post(self, request, *args, **kwargs):
        """Allow users to click an ad"""
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad clicked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveAdView(ListCreateAPIView):
    """Allow users to save an ad for later"""
    serializer_class = SaveAdSerializer
    queryset = AdSaved.objects.all()
    permission_classes = [IsAuthenticated]

    extend_schema(
        tags=['Advertisements'],
        summary="List saved ads",
        description="Retrieve a list of ads saved by the authenticated user.",
        responses={200: SaveAdSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Save an ad",
        description="Save an ad by providing its ID. Returns a success message if saved successfully.",
        request=SaveAdSerializer,
        responses={201: {"message": "Ad saved successfully"}, 400: "Validation errors"}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





