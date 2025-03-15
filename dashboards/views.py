from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from beacons.models import Beacon
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from beacon_messages.models import BeaconMessage
from beacon_messages.serializers import BeaconMessageCountSerializer
from logs.models import AdvertisementLog
from django.utils.timezone import now, timedelta

class BeaconCount(APIView):
    """Retrieve the total count of beacons."""

    # permission_classes = [IsAuthenticated]  # Enforce authentication

    @extend_schema(
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

    extend_schema(
        summary="Retrieve beacon message counts per day",
        description="Returns a list of beacons with the total number of beacon_messages sent each day.",
        parameters=[
            OpenApiParameter(
                name="date",
                type=str,
                description="Filter results by a specific date (YYYY-MM-DD). Example: ?date=2025-03-06",
                required=False
            ),
        ],
        responses={200: BeaconMessageCountSerializer(many=True)},
    )

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

class LogCount(APIView):
    """Count advertisement logs for the past 24 hours. """

    @extend_schema(
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
            return Response({'message': 'No ads found'}, status=404)

        return Response({"count": recent_advertisements, "message": f"Found {recent_advertisements} ads."}, status=200)