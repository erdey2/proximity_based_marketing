from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from rest_framework.response import Response
from campaign.models import Advertisements
from campaign.serializers import AdvertisementsSerializer
from django.utils.timezone import now
import uuid
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class AdvertisementRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Custom throttle rate for this view

@throttle_classes([AdvertisementRateThrottle, AnonRateThrottle])
@api_view(['GET', 'POST'])
def advertisements_list(request):
    """
    list all advertisements or create a new one
    """
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
def advertisements_detail(request, pk):
    """
    Retrieve, update, or delete an advertisement item
    """
    try:
        advertisement = Advertisements.objects.get(pk=pk)
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
def advertisements_search(request):
    """
    search for advertisements based on query parameters (title)
    """
    title = request.query_params.get('title', None)
    # start with all advertisements
    advertisements = Advertisements.objects.all()
    if title:
        advertisements = Advertisements.objects.filter(title__icontains=title)

    if not advertisements.exists():  # Check if the queryset is empty
        return Response({"message": "No advertisements found matching the query."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the filtered advertisements
    serializer = AdvertisementsSerializer(advertisements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def advertisements_active(request):
    """
    List all active advertisements
    """
    current_time = now()  # Get the current datetime
    advertisements = Advertisements.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    serializer = AdvertisementsSerializer(advertisements, many=True)
    return Response(serializer.data)
