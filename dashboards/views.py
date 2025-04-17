from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from beacons.models import Beacon
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from beacon_messages.models import BeaconMessage
from beacon_messages.serializers import BeaconMessageCountSerializer
from logs.models import AdvertisementLog
from django.utils.timezone import now, timedelta
from advertisements.models import Advertisement, AdView, AdClick, AdSaved, AdLike
from advertisements.serializers import AdvertisementSerializer, AdInteractionSerializer
from advertisements.views import CustomPagination


class BeaconCount(APIView):
    """Retrieve the total count of beacons."""

    @extend_schema(
        tags=['Analytics'],
        summary="Retrieve Total Beacon Count",
        description="""
        This endpoint allows authenticated users to retrieve the total count of beacons in the system.

        **Methods:**
        - `GET`: Returns the total number of beacons.

        **Example Use Case:**
        - A system admin wants to monitor the number of beacons.

        **Validation:**
        - Authentication is required (`IsAuthenticated`).
        - If no beacons are found, an appropriate response is returned.
        """,
        responses={
            200: {
                "count": "integer (total number of beacons)",
                "message": "string (description of beacon count)"
            },
            204: {"message": "No beacons available."},
            401: {"detail": "Authentication credentials were not provided."}
        },
    )
    def get(self, request):
        total_beacons = Beacon.objects.count()
        if total_beacons == 0:
            return Response({'message': 'No beacons available.'}, status=status.HTTP_204_NO_CONTENT)

        return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."},
                        status=status.HTTP_200_OK)

class BeaconLocationCount(APIView):
    """API endpoint to count the total number of unique beacon locations."""

    # permission_classes = [IsAuthenticated]  # Enforce authentication
    @extend_schema(
        tags=['Analytics'],
        summary="Get Total Unique Beacon Locations",
        description="Returns the total number of unique beacon locations in the system.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "total_locations": {
                        "type": "integer",
                        "example": 8
                    }
                }
            },
            204: {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "No beacon locations found"
                    }
                }
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided."
                    }
                }
            }
        }
    )
    def get(self, request):
        total_locations = Beacon.objects.exclude(location_name__isnull=True).values('location_name').distinct().count()

        if total_locations == 0:
            return Response({'message': 'No beacon locations found'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'total_locations': total_locations}, status=status.HTTP_200_OK)

class BeaconMessageCountView(generics.ListAPIView):
    """ API endpoint to get the total beacon_messages sent by each beacon per day. """
    serializer_class = BeaconMessageCountSerializer

    def get_queryset(self):
        """Filter beacon_messages based on the optional `date` query parameter."""
        date_filter = self.request.GET.get('date')

        queryset = BeaconMessage.objects.all()
        if date_filter:
            queryset = queryset.filter(sent_at__date=date_filter)

        return (
            queryset.values('beacon__beacon_id', 'beacon__name', date=TruncDate('sent_at'))
            .annotate(total_messages=Count('message_id'))
            .order_by('date')
        )

    @extend_schema(
        tags=['Analytics'],
        summary="Retrieve beacon message counts per day",
        description="Returns a list of beacons with the total number of beacon messages sent each day. "
                    "Optionally, filter results by a specific date.",
        parameters=[
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
                description="Filter results by a specific date (YYYY-MM-DD). Example: ?date=2025-03-06",
                required=False
            ),
        ],
        responses={200: BeaconMessageCountSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """Retrieve total beacon message counts per beacon per day."""
        return self.list(request, *args, **kwargs)

class LogCount(APIView):
    """Count advertisement logs for the past 24 hours. """

    @extend_schema(
        tags=['Analytics'],
        summary="Count advertisement logs for the past 24 hours",
        description="This endpoint counts the number of advertisement logs created in the past 24 hours.",
        responses={
            200: {
                "message": "Advertisement log count for the past 24 hours",
                "count": "integer"
            },
            404: {
                "message": "No advertisement logs found for the past 24 hours"
            }
        },
    )
    def get(self, request, *args, **kwargs):
        # Calculate 24 hours ago from the current time
        start_date = now() - timedelta(days=1)
        # Count the advertisement logs created in the past 24 hours
        recent_advertisements = AdvertisementLog.objects.filter(timestamp__gte=start_date).count()

        if not recent_advertisements:
            return Response({'message': 'No logs found'}, status=404)

        return Response({"count": recent_advertisements, "message": f"Found {recent_advertisements} logs."}, status=200)

class PopularAdsView(generics.ListAPIView):
    """Fetch top 10 most viewed ads in the last 7 days."""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Analytics"],
        summary="Get Top 10 Popular Ads",
        description="Returns the top 10 most viewed advertisements in the past 7 days, "
                    "ranked by view count. You can optionally filter ads using the `search` query "
                    "parameter, which matches both title and content.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search term to filter ads by title or content",
                required=False,
                type=str
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="List of top 10 most viewed ads with interaction data."
            ),
            400: OpenApiResponse(description="Bad Request")
        }
    )
    def get_queryset(self):
        last_week = now() - timedelta(days=7)
        qs = Advertisement.objects.all()

        # Optional search filtering
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        # Annotate with view count and order
        popular_ads = qs.annotate(
            engagement_score=Count(
                'views',
                filter=Q(views__viewed=True, views__viewed_at__gte=last_week)
            )
        ).order_by('-engagement_score', '-created_at')[:10]

        return popular_ads

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user
        result = []

        for ad in queryset:
            view = AdView.objects.filter(user=user, ad=ad).first()
            like = AdLike.objects.filter(user=user, ad=ad).first()
            click = AdClick.objects.filter(user=user, ad=ad).first()
            save = AdSaved.objects.filter(user=user, ad=ad).first()

            data = {
                'ad': AdvertisementSerializer(ad, context={'request': request}).data,
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

        page = self.paginate_queryset(result)
        return self.get_paginated_response(page)

class ClicksPerDayAPIView(APIView):
    """
    Retrieve the number of ad clicks per day.
    """
    @extend_schema(
        tags=['Analytics'],
        summary="Retrieve Clicks Per Day",
        description="Returns the number of advertisement clicks per day, grouped by date.",
        responses={200:
            {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "clicked_at": {
                            "type": "string",
                            "format": "date",
                            "example": "2025-04-01"
                        },
                        "total_clicks": {
                            "type": "integer",
                            "example": 25
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        clicks_per_day = AdClick.objects.annotate(date=TruncDate('clicked_at')) \
                                      .values('clicked_at') \
                                      .annotate(total_clicks=Count('ad')) \
                                      .order_by('-clicked_at')

        return Response(clicks_per_day)

class ImpressionsPerDayAPIView(APIView):
    """
    Retrieve the number of ad views per day.
    """
    @extend_schema(
        tags=['Analytics'],
        summary="Retrieve impressions Per Day",
        description="Returns the number of advertisement views per day, grouped by date.",
        responses={200:
            {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "viewed_at": {
                            "type": "string",
                            "format": "date",
                            "example": "2025-04-01"
                        },
                        "total_views": {
                            "type": "integer",
                            "example": 25
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        views_per_day = AdView.objects.annotate(date=TruncDate('viewed_at')) \
                                      .values('viewed_at') \
                                      .annotate(total_views=Count('ad')) \
                                      .order_by('-date')

        return Response(views_per_day)

