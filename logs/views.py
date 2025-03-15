from logs.models import AdvertisementLog
from .serializers import AdvertisementLogSerializer, AdvertisementLogPartialSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from datetime import datetime

class LogList(ListCreateAPIView):
    """List all Advertisement Logs or create a new one."""
    serializer_class = AdvertisementLogSerializer

    def get_queryset(self):
        qs = AdvertisementLog.objects.select_related('advertisement', 'beacon').all()
        log_id = self.request.GET.get('log_id')
        created_at = self.request.GET.get('created_at')

        if log_id:
            qs = qs.filter(log_id__contains=log_id)
        if created_at:
            try:
                parsed_created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
                qs = qs.filter(created_at__gte=parsed_created_at)
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
        return qs

    @extend_schema(
        summary="Retrieve Advertisement Logs",
        description="""
            Retrieve a paginated list of all advertisement logs, with optional filtering by `log_id` and `created_at`.
            **Example Response:**
            ```json
            {
                "log_id": "LOG123",
                "created_at": "2024-02-23",
                "advertisement_title": "New Year Sale",
                "beacon_name": "Beacon A"
            }
            ```
        """,
        parameters=[
            OpenApiParameter(name="log_id", description="Filter by log ID", required=False, type=str),
            OpenApiParameter(name="created_at", description="Filter by created date (YYYY-MM-DD)", required=False, type=str),
        ],
        responses={200: AdvertisementLogSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new Advertisement Log",
        description="""
            Create a new advertisement log entry when a beacon sends an advertisement.  
            The log records details such as which advertisement was sent, the beacon that sent it, 
            and the timestamp of the event.

            **Example Request:**
            ```json
            {
                "log_id": "LOG123",
                "advertisement": 1,
                "beacon": 2,
                "created_at": "2024-03-08T12:30:00Z"
            }
            ```

            **Example Response (201 Created):**
            ```json
            {
                "log_id": "LOG123",
                "advertisement": 1,
                "beacon": 2,
                "created_at": "2024-03-08T12:30:00Z"
            }
            ```
        """,
        request=AdvertisementLogSerializer,
        responses={
            201: AdvertisementLogSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data format"),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class LogDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementLogSerializer
    queryset = AdvertisementLog.objects.all()

    @extend_schema(
        summary="Retrieve an Advertisement Log",
        description="""
                Get details of a specific advertisement log by its ID.

                **Example Response (200 OK):**
                ```json
                {
                    "log_id": "LOG123",
                    "advertisement": 1,
                    "beacon": 2,
                    "created_at": "2024-03-08T12:30:00Z"
                }
                ```
            """,
        responses={200: AdvertisementLogSerializer, 404: OpenApiResponse(description="Not Found")}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement Log",
        description="""
                Replace an existing advertisement log entry with new data.

                **Example Request:**
                ```json
                {
                    "log_id": "LOG123",
                    "advertisement": 2,
                    "beacon": 3,
                    "created_at": "2024-03-09T10:00:00Z"
                }
                ```

                **Example Response (200 OK):**
                ```json
                {
                    "log_id": "LOG123",
                    "advertisement": 2,
                    "beacon": 3,
                    "created_at": "2024-03-09T10:00:00Z"
                }
                ```
            """,
        request=AdvertisementLogSerializer,
        responses={200: AdvertisementLogSerializer, 400: OpenApiResponse(description="Bad Request")}

    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement Log",
        description="""
                Update specific fields of an advertisement log without replacing the entire entry.

                **Example Request:**
                ```json
                {
                    "advertisement": 3
                }
                ```

                **Example Response (200 OK):**
                ```json
                {
                    "log_id": "LOG123",
                    "advertisement": 3,
                    "beacon": 2,
                    "created_at": "2024-03-08T12:30:00Z"
                }
                ```
            """,
        request=AdvertisementLogSerializer,
        responses={200: AdvertisementLogPartialSerializer, 400: OpenApiResponse(description="Bad Request")}

    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an Advertisement Log",
        description="Delete a specific advertisement log by ID.",
        responses={204: OpenApiResponse(description="No Content"), 404: OpenApiResponse(description="Not Found")}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
