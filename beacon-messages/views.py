from beacon_messages.models import BeaconMessage
from .serializers import BeaconMessageSerializer, BeaconMessageCountSerializer
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter

class MessageList(generics.ListCreateAPIView):
    """Create and List beacon-messages from beacons"""
    serializer_class = BeaconMessageSerializer

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
        summary="List all beacon-messages sent by beacons",
        description="Retrieve a list of all existing beacon-messages. Optionally, filter by 'sent_at' date parameter.",
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
        summary="Create a new beacon message",
        description="""
            This endpoint allows creating a new message sent by a beacon. 
            The request should include details such as the beacon ID, message content, 
            and timestamp when the message was sent.

            **Example Request:**
            ```json
            {
                "beacon": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Special discount available!",
                "sent_at": "2025-03-08T12:30:00Z"
            }
            ```
        """,
        request=BeaconMessageSerializer,
        responses={
            201: {
                "description": "Message successfully created.",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "beacon": "123e4567-e89b-12d3-a456-426614174000",
                            "message": "Special discount available!",
                            "sent_at": "2025-03-08T12:30:00Z"
                        }
                    }
                }
            },
            400: {
                "description": "Bad request. Invalid or missing data.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Invalid beacon ID or missing required fields."}
                    }
                }
            }
        },

    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get and delete beacon-messages"""
    queryset = BeaconMessage.objects.all()
    serializer_class = BeaconMessageSerializer

    @extend_schema(
        summary="Retrieve a specific beacon message",
        description="Fetch the details of a single beacon message by its ID.",
        responses={
            200: BeaconMessageSerializer,
            404: {
                "description": "Message not found.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Not found."}
                    }
                }
            }
        },
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a beacon message",
        description="""
            Replace the entire message object with a new one.

            **Example Request:**
            ```json
            {
                "beacon": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Updated advertisement message!",
                "sent_at": "2025-03-08T15:45:00Z"
            }
            ```
        """,
        request=BeaconMessageSerializer,
        responses={
            200: BeaconMessageSerializer,
            400: {
                "description": "Bad request. Invalid or missing data.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Invalid beacon ID or missing required fields."}
                    }
                }
            }
        },

    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a beacon message",
        description="""
            Update specific fields of a beacon message without replacing the whole object.

            **Example Request:**
            ```json
            {
                "message": "Limited-time offer!"
            }
            ```
        """,
        request=BeaconMessageSerializer(partial=True),
        responses={
            200: BeaconMessageSerializer,
            400: {
                "description": "Bad request. Invalid or missing data.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Invalid data provided."}
                    }
                }
            }
        },

    )
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a beacon message",
        description="Remove a beacon message from the system permanently.",
        responses={
            204: {
                "description": "Message successfully deleted."
            },
            404: {
                "description": "Message not found.",
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
