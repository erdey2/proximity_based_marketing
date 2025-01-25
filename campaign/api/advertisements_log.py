from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from campaign.models import AdvertisementsLog
from campaign.serializers import AdvertisementsLogsSerializer
from django.utils.timezone import now, timedelta

@api_view(['GET', 'POST'])
def log_list(request):
    """
    list all advertisement logs or create a new one
    """
    if request.method == 'GET':
        logs = AdvertisementsLog.objects.all()
        serializers = AdvertisementsLogsSerializer(logs, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = AdvertisementsLogsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def log_count(request):
    # Count for the past 24 hours
    start_date = now() - timedelta(days=1)
    recent_advertisements = AdvertisementsLog.objects.filter(timestamp__gte=start_date).count()
    if not recent_advertisements:
        return Response({'message': 'No ads found'}, status=404)
    return Response({"count": recent_advertisements, "message": f"Found {recent_advertisements} ads."}, status=200)

