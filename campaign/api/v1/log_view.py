from campaign.models import AdvertisementLog
from campaign.serializers import AdvertisementLogSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from drf_spectacular.utils import extend_schema
from datetime import datetime

class LogPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 50
    display_page_controls = False
    invalid_page_message = 'invalid page'

class LogList(ListCreateAPIView):
    """List all Advertisement Logs or create a new one."""
    serializer_class = AdvertisementLogSerializer
    pagination_class = LogPagination

    def get_queryset(self):
        qs = AdvertisementLog.objects.all()
        log_id = self.request.GET.get('log_id')
        created_at = self.request.GET.get('created_at')

        if log_id:
            qs = qs.filter(log_id__contains=log_id)
        if created_at:
            try:
                # Parse 'created_at' parameter to date
                parsed_created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
                # Filter queryset by 'sent_at' greater than or equal to parsed date
                qs = qs.filter(created_at__gte=parsed_created_at)
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
        return qs

    extend_schema(
        summary="Retrieve Advertisement Logs",
        description="""
                Retrieve a paginated list of all advertisement logs, with optional filtering by `log_id` and `created_at`.

                **Example Request:**
                ```
                GET /api/logs/?log_id=123&created_at=2024-01-01
                ```
            """,
        responses={200: AdvertisementLogSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Advertisement Log",
        description="Create a new advertisement log with the provided data.",
        request=AdvertisementLogSerializer,
        responses={
            201: AdvertisementLogSerializer,
            400: {"message": "Invalid input data."},
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class LogDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementLogSerializer
    queryset = AdvertisementLog.objects.all()

    @extend_schema(
        summary="Retrieve a Single Advertisement Log",
        description="Retrieve the details of a specific advertisement log by providing its ID.",
        responses={200: AdvertisementLogSerializer, 404: {"message": "Not Found"}},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an Advertisement Log",
        description="Update an advertisement log by providing its ID and new data.",
        request=AdvertisementLogSerializer,
        responses={200: AdvertisementLogSerializer, 400: {"message": "Bad Request"}, 404: {"message": "Not Found"}},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update an Advertisement Log",
        description="Partially update an advertisement log by providing only the fields that need to be changed.",
        request=AdvertisementLogSerializer(partial=True),
        responses={200: AdvertisementLogSerializer, 400: {"message": "Bad Request"}, 404: {"message": "Not Found"}},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an Advertisement Log",
        description="Delete a specific advertisement log by providing its ID.",
        responses={204: None, 404: {"message": "Not Found"}},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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




