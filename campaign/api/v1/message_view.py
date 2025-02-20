from campaign.models import BeaconMessage
from campaign.serializers import BeaconMessageSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 2 # Customize page size
    page_query_param = 'page_size' # Allow clients to specify page size
    max_page_size = 50  # Limit maximum page size

class MessageCreate(generics.ListCreateAPIView):
    """Create and List messages from beacons"""
    serializer_class = BeaconMessageSerializer
    pagination_class = MessagePagination # apply pagination

    def get_queryset(self):
        qs = BeaconMessage.objects.all()
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

    summary = "List all messages sent by beacons",
    description = "Retrieve a list of all existing messages. Optionally, filter by 'sent_at' date parameter.",
    responses = {
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
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new message",
        description="Create a new message with the provided data.",
        request=BeaconMessageSerializer,
        responses={201: BeaconMessageSerializer},
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

