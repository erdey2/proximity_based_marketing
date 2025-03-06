from django.db.models import Count
from django.db.models.functions import TruncDate

from campaign.models import BeaconMessage
from campaign.serializers import BeaconMessageSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter

class MessagePagination(PageNumberPagination):
    page_size = 2 # Customize page size
    page_query_param = 'page_size' # Allow clients to specify page size
    max_page_size = 50  # Limit maximum page size

class MessageList(generics.ListCreateAPIView):
    """Create and List messages from beacons"""
    serializer_class = BeaconMessageSerializer
    pagination_class = MessagePagination  # Apply pagination

    def get_queryset(self):
        qs = BeaconMessage.objects.select_related('beacon').all()  # Optimize query
        sent_at = self.request.GET.get('sent_at')
        if sent_at:
            try:
                # Parse 'sent_at' parameter to date
                parsed_sent_at = datetime.strptime(sent_at, "%Y-%m-%d").date()
                # Filter queryset by 'sent_at' greater than or equal to parsed date
                qs = qs.filter(sent_at__gte=parsed_sent_at)
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
        return qs

    @extend_schema(
        summary="List all messages sent by beacons",
        description="Retrieve a list of all existing messages. Optionally, filter by 'sent_at' date parameter.",
        parameters=[
            OpenApiParameter(name="sent_at", description="Filter by sent date (YYYY-MM-DD)", required=False, type=str),
        ],
        responses={
            200: BeaconMessageSerializer(many=True),
            400: {
                "description": "Bad request. Invalid date format provided for 'sent_at'.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Invalid date format. Use YYYY-MM-DD."}
                    }
                }
            }
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new message",
        description="Create a new message with the provided data.",
        request=BeaconMessageSerializer,
        responses={
            201: BeaconMessageSerializer,
            400: {"description": "Invalid input data."},
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get and delete messages"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer

    @extend_schema(
        summary="Retrieve a specific Beacon Message",
        description="Retrieve a Beacon Message by its ID.",
        responses={200: BeaconMessageSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement Log",
        description="Replace an existing advertisement log with the provided data.",
        request=BeaconMessageSerializer,
        responses={
            200: BeaconMessageSerializer,
            400: {"message": "Bad Request"},
            404: {"message": "Not Found"},
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement Log",
        description="Update specific fields of an advertisement log.",
        request=BeaconMessageSerializer(partial=True),
        responses={
            200: BeaconMessageSerializer,
            400: {"message": "Bad Request"},
            404: {"message": "Not Found"},
        },
    )
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a specific Beacon Message",
        description="Delete a Beacon Message by its ID.",
        responses={
            204: None,
            404: {
                "description": "Not Found. The specified Beacon Message does not exist.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Not found."}
                    }
                }
            }
        },
    )
    def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

class BeaconMessageCountView(generics.ListAPIView):
    """ API endpoint to get the total messages sent by each beacon per day. """
    extend_schema(
        summary="Retrieve beacon message counts per day",
        description="Returns a list of beacons with the total number of messages sent each day.",
        parameters=[
            OpenApiParameter(
                name="date",
                type=str,
                description="Filter results by a specific date (YYYY-MM-DD). Example: ?date=2025-03-06",
                required=False
            ),
        ],
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "beacon__beacon_id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "beacon__name": {"type": "string", "example": "Beacon A"},
                        "date": {"type": "string", "format": "date", "example": "2025-03-06"},
                        "total_messages": {"type": "integer", "example": 10},
                    },
                },
            },
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Returns the total number of messages sent by each beacon per day.
        Optional: Filter by date using the query parameter `?date=YYYY-MM-DD`.
        """
        date_filter = request.GET.get('date')

        queryset = BeaconMessage.objects.all()

        if date_filter:
            queryset = queryset.filter(sent_at__date=date_filter)

        message_counts = (
            queryset.values('beacon__beacon_id', 'beacon__name', date=TruncDate('sent_at'))
            .annotate(total_messages=Count('message_id'))
            .order_by('date')
        )

        return Response(message_counts)


