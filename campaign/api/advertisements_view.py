from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from campaign.models import Advertisements
from campaign.serializers import AdvertisementsSerializer
from django.utils.timezone import now
import uuid

@api_view(['GET', 'POST'])
def advertisements_list(request):
    # list all advertisements or create a new one
    if request.method == 'GET':
        advertisements = Advertisements.objects.all()
        serializer = AdvertisementsSerializer(advertisements, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AdvertisementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def advertisements_detail(request, uuid):
    """
    Retrieve, update, or delete an advertisement item
    """
    try:
        advertisement = Advertisements.objects.get(uuid=uuid)
    except Advertisements.DoesNotExist:
        return Response({"error": "Advertisement not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdvertisementsSerializer(advertisement)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AdvertisementsSerializer(advertisement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        advertisement.delete()
        return Response(status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def advertisements_active(request):
    """
    List all active advertisements
    """
    current_time = now()  # Get the current datetime
    advertisements = Advertisements.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    serializer = AdvertisementsSerializer(advertisements, many=True)
    return Response(serializer.data)
