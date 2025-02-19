from campaign.models import AdvertisementLog
from campaign.serializers import AdvertisementLogSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from drf_spectacular.utils import extend_schema


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
            return qs
        if created_at:
            qs = qs.filter(timestamp__icontains=created_at)
        return qs

    @extend_schema(
        summary="Retrieve Advertisement Logs",
        description="Retrieve a paginated list of all advertisement logs.",
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


class LogsCount(RetrieveAPIView):
    """Count advertisement logs for the past 24 hours. """

    @extend_schema(
        summary="Count advertisement logs for the past 24 hours",
        description="This endpoint counts the number of advertisement logs created in the past 24 hours",
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
    def retrieve(self, request, *args, **kwargs):
        start_date = now() - timedelta(days=1)
        recent_advertisements = AdvertisementLog.objects.filter(timestamp__gte=start_date).count()

        if not recent_advertisements:
            return Response({'message': 'No ads found'}, status=404)

        return Response({
            "count": recent_advertisements,
            "message": f"Found {recent_advertisements} ads."
        }, status=200)




