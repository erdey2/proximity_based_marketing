from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Advertisement
from .serializers import (AdvertisementSerializer, AdvertisementSimpleSerializer, AdvertisementTitleSerializer,
                          AdInteractionSerializer, LikedSavedAdSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
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

class CustomPagination(PageNumberPagination):
        page_size = 3  # Default items per page
        page_query_param = 'page'  # ?page=2
        page_size_query_param = 'page_size'  # Allows users to set page size dynamically
        max_page_size = 100  # Maximum allowed page size

        def paginate_queryset(self, queryset, request, view=None):
            """Override pagination to handle out-of-range pages gracefully."""
            try:
                return super().paginate_queryset(queryset, request, view)
            except NotFound:
                self.page = None  # Prevents `get_paginated_response` from crashing
                return []  # Return empty list when page is out of range

        def get_paginated_response(self, data):
            """Return custom paginated response."""
            return Response({
                "count": getattr(self.page.paginator, "count", 0) if self.page else 0,  # Avoid AttributeError
                "next": self.get_next_link() if self.page else None,
                "previous": self.get_previous_link() if self.page else None,
                "results": data  # Empty list if page is out of range
            }, status=200)  # Always return HTTP 200

class AdvertisementList(ListCreateAPIView):
    """ List all advertisements or create a new one. """
    serializer_class = AdvertisementSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allows image uploads

    def get_queryset(self):
        qs = Advertisement.objects.all()

        # Use a single query parameter 'search' for both title and content
        query = self.request.GET.get('search')

        if query:
            search_conditions = Q(title__icontains=query) | Q(content__icontains=query)
            qs = qs.filter(search_conditions)

        return qs

    @extend_schema(
        tags=["Advertisements"],
        summary="List Advertisements",
        description="Retrieve a list of advertisements. You can optionally search by title or content using the `search` query parameter.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Search term to filter advertisements by title or content.",
            ),
            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Page number for pagination.",
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Number of items per page.",
            ),
        ],
        responses={200: AdvertisementSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Advertisements"],
        summary="Create Advertisement",
        description="Create a new advertisement. Supports image uploads via multipart form data.",
        request=AdvertisementSerializer,
        responses={201: AdvertisementSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementListWithPagination(ListCreateAPIView):
    """List all advertisements or create a new one."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all().order_by('created_at')
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Advertisement.objects.all()

        # Use a single query parameter 'search' for both title and content
        query = self.request.GET.get('search')

        if query:
            search_conditions = Q(title__icontains=query) | Q(content__icontains=query)
            qs = qs.filter(search_conditions)

        return qs

    @extend_schema(
        tags=["Advertisements"],
        summary="List Advertisements with Pagination",
        description="Retrieve a paginated list of advertisements. Supports filtering by title or content using the `search` query parameter.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Search advertisements by title or content.",
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Page number for pagination.",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Number of results per page.",
            ),
        ],
        responses={200: AdvertisementSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Advertisements"],
        summary="Create Advertisement",
        description="Create a new advertisement. You can upload images using multipart form data.",
        request=AdvertisementSerializer,
        responses={201: AdvertisementSerializer},
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
            200: AdInteractionSerializer,
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

class ViewAdListView(ListCreateAPIView):
    """Allow users to view an ad and retrieve their viewed ads, with optional search functionality."""
    serializer_class = ViewAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return the viewed ads of the authenticated user, optionally filtered by a search query."""
        # Start with the queryset of ads viewed by the authenticated user
        viewed_ads = Advertisement.objects.filter(adview__user=self.request.user)

        # Retrieve the search query parameter
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filter advertisements by title or content containing the search term
            viewed_ads = viewed_ads.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return viewed_ads

    @extend_schema(
        tags=["Advertisements"],
        summary="List viewed ads",
        description=(
                "Retrieves a list of advertisements that the authenticated user has viewed. "
                "Supports optional filtering by a search query parameter to match advertisement titles or content."
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                description='A search term to filter advertisements by title or content.',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: ViewAdSerializer(many=True),
            401: {
                'description': 'Unauthorized - Authentication credentials were not provided or are invalid.',
            },
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Mark an ad as viewed",
        description="Allows an authenticated user to mark a specific ad as viewed.",
        request=ViewAdSerializer,
        responses={
            201: OpenApiResponse(
                description="Ad viewed successfully",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success',
                        value={"message": "Ad viewed successfully"},
                        response_only=True,
                        status_codes=["201"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Validation Error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={"ad_id": ["This field is required."]},
                        response_only=True,
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                'Request Example',
                value={
                    "ad_id": "e97d5b0e-1d7a-4a87-9a68-54876b6e9e23",
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        """Allow users to view an ad"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad viewed successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeAdView(ListCreateAPIView):
    """Allow users to like an ad and retrieve their liked ads, with optional search functionality."""
    serializer_class = LikeAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return the liked ads of the authenticated user, optionally filtered by a search query."""
        # Start with the queryset of ads liked by the authenticated user
        liked_ads = Advertisement.objects.filter(likes__user=self.request.user)

        # Retrieve the search query parameter
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filter advertisements by title or content containing the search term
            liked_ads = liked_ads.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return liked_ads

    @extend_schema(
        tags=["Advertisements"],
        summary="List liked ads",
        description=(
                "Retrieves a list of advertisements that the authenticated user has liked. "
                "Supports optional filtering by a search query parameter to match advertisement titles or content."
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                description='A search term to filter advertisements by title or content.',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: AdInteractionSerializer(many=True),
            401: {
                'description': 'Unauthorized - Authentication credentials were not provided or are invalid.',
            },
        },

    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Like an advertisement",
        description="Allows an authenticated user to like a specific advertisement by submitting its `ad_id`.",
        request=LikeAdSerializer,
        responses={
            201: OpenApiResponse(
                description="Ad liked successfully",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={"message": "Ad liked successfully"},
                        response_only=True,
                        status_codes=["201"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Validation error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Missing ad_id",
                        value={"ad_id": ["This field is required."]},
                        response_only=True,
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                name="Like Request Example",
                value={
                    "ad_id": "2a6f188b-1234-4abc-a456-7f2f42c31e89",
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        """Allow users to like an ad"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad liked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClickAdView(ListCreateAPIView):
    """Allow users to click an ad and retrieve their clicked ads, with optional search functionality."""
    serializer_class = ClickAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return the viewed ads of the authenticated user, optionally filtered by a search query."""
        # Start with the queryset of ads clicked by the authenticated user
        clicked_ads = Advertisement.objects.filter(clicks__user=self.request.user)

        # Retrieve the search query parameter
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filter advertisements by title or content containing the search term
            clicked_ads = clicked_ads.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return clicked_ads

    @extend_schema(
        tags=["Advertisements"],
        summary="List clicked ads",
        description=(
                "Retrieves a list of advertisements that the authenticated user has clicked. "
                "Supports optional filtering by a search query parameter to match advertisement titles or content."
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                description='A search term to filter advertisements by title or content.',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: ViewAdSerializer(many=True),
            401: {
                'description': 'Unauthorized - Authentication credentials were not provided or are invalid.',
            },
        },

    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Click an advertisement",
        description="Allows an authenticated user to register a click on a specific advertisement by providing its `ad_id`.",
        request=ClickAdSerializer,
        responses={
            201: OpenApiResponse(
                description="Ad clicked successfully",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={"message": "Ad clicked successfully"},
                        response_only=True,
                        status_codes=["201"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Validation error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Invalid Data",
                        value={"ad_id": ["This field is required."]},
                        response_only=True,
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                name="Click Request Example",
                value={
                    "ad_id": "3c9ef5e0-2d1b-47c2-9d60-2b76d6e3f404",
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        """Allow users to click an ad"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad clicked successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaveAdView(ListCreateAPIView):
    """Allow users to save an ad and retrieve their saved ads, with optional search functionality."""
    serializer_class = SaveAdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return the saved ads of the authenticated user, optionally filtered by a search query."""
        # Start with the queryset of ads saved by the authenticated user
        saved_ads = Advertisement.objects.filter(saves__user=self.request.user)

        # Retrieve the search query parameter
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filter advertisements by title or content containing the search term
            saved_ads = saved_ads.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return saved_ads

    @extend_schema(
        tags=["Advertisements"],
        summary="List saved ads",
        description=(
                "Retrieves a list of advertisements that the authenticated user has saved."
                "Supports optional filtering by a search query parameter to match advertisement titles or content."
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                description='A search term to filter advertisements by title or content.',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: ViewAdSerializer(many=True),
            401: {
                'description': 'Unauthorized - Authentication credentials were not provided or are invalid.',
            },
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Advertisements'],
        summary="Save an advertisement",
        description="Allows an authenticated user to save a specific advertisement by providing its `ad_id`. This helps users bookmark ads for later viewing.",
        request=SaveAdSerializer,
        responses={
            201: OpenApiResponse(
                description="Ad saved successfully",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={"message": "Ad saved successfully"},
                        response_only=True,
                        status_codes=["201"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Validation error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Missing ad_id",
                        value={"ad_id": ["This field is required."]},
                        response_only=True,
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                name="Save Request Example",
                value={
                    "ad_id": "f51acb8b-56f3-4c20-bf99-73f74805be23",
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        """Allow users to click an ad"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ad saved successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedSavedAdsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Advertisements"],
        summary="Get liked and saved ads",
        description="Returns a list of ads liked or saved by the authenticated user, with optional search.",
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Search ads by title or content.'
            )
        ],
        responses={
            200: OpenApiResponse(response=LikedSavedAdSerializer(many=True)),
            401: OpenApiResponse(description="Authentication required.")
        }
    )
    def get(self, request):
        user = request.user
        search_query = request.GET.get('search', '')

        liked_ads = AdLike.objects.select_related('ad').filter(user=user, liked=True)
        saved_ads = AdSaved.objects.select_related('ad').filter(user=user, saved=True)

        ad_map = {}

        # Collect liked ads
        for like in liked_ads:
            if search_query and search_query.lower() not in (like.ad.title.lower() + like.ad.content.lower()):
                continue
            ad_map[like.ad.advertisement_id] = {
                'ad': AdvertisementSerializer(like.ad).data,
                'liked': like.liked,
                'liked_at': like.liked_at,
                'saved': False,
                'saved_at': None,
            }

        # Merge with saved ads
        for save in saved_ads:
            if search_query and search_query.lower() not in (save.ad.title.lower() + save.ad.content.lower()):
                continue
            if save.ad.id in ad_map:
                ad_map[save.ad.id]['saved'] = save.saved
                ad_map[save.ad.id]['saved_at'] = save.saved_at
            else:
                ad_map[save.ad.id] = {
                    'ad': AdvertisementSerializer(save.ad).data,
                    'liked': False,
                    'liked_at': None,
                    'saved': save.saved,
                    'saved_at': save.saved_at,
                }

        return Response(list(ad_map.values()))

class AdInteractionView(APIView):
    """Retrieve all ads with user interactions (viewed, liked, clicked, saved). """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Return the saved ads of the authenticated user, optionally filtered by a search query."""
        # Start with the queryset of ads saved by the authenticated user
        interaction_ads = Advertisement.objects.filter(adinteraction__user=self.request.user)

        # Retrieve the search query parameter
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filter advertisements by title or content containing the search term
            interaction_ads = interaction_ads.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return interaction_ads

    @extend_schema(
        tags=["Advertisements"],
        summary="Get ads with user interactions",
        description=(
                "Returns a list of ads that the authenticated user has interacted with, "
                "including viewed, liked, clicked, and saved statuses and timestamps.\n\n"
                "Supports optional search by ad title or content."
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filter ads by title or content.'
            )
        ],
        responses={
            200: OpenApiResponse(
                description="List of ads with user interaction data.",
                response=AdInteractionSerializer(many=True)
            ),
            401: OpenApiResponse(description="Unauthorized. User must be authenticated.")
        }

    )
    def get(self, request):
        user = request.user
        ads = Advertisement.objects.all()
        result = []

        for ad in ads:
            view = AdView.objects.filter(user=user, ad=ad).first()
            like = AdLike.objects.filter(user=user, ad=ad).first()
            click = AdClick.objects.filter(user=user, ad=ad).first()
            save = AdSaved.objects.filter(user=user, ad=ad).first()

            data = {
                'ad': AdvertisementSerializer(ad).data,
                'viewed': view.viewed if view else False,
                'viewed_at': view.viewed_at if view else None,
                'liked': like.liked if like else False,
                'liked_at': like.liked_at if like else None,
                'clicked': click.clicked if click else False,
                'clicked_at': click.clicked_at if click else None,
                'saved': save.saved if save else False,
                'saved_at': save.saved_at if save else None,
            }

            result.append(data)

        return Response(result)




