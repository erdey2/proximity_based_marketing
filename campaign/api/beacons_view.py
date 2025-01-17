from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView
from campaign.models import Beacons
from campaign.serializers import BeaconsSerializer

class AllBeacons(ListAPIView):
    queryset = Beacons.objects.all()
    serializer_class = BeaconsSerializer

@api_view(['GET', 'POST'])
def beacons_list(request):
    """
    list all beacons or create a new one
    """
    if request.method == 'GET':
        beacons = Beacons.objects.all()
        serializer = BeaconsSerializer(beacons, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BeaconsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def beacons_detail(request, uuid):
    """
    Retrieve, update, or delete beacon item
    """
    try:
        beacon = Beacons.objects.get(uuid=uuid)
    except Beacons.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BeaconsSerializer(beacon)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BeaconsSerializer(beacon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        beacon.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def beacons_search(request):
    """
    search for beacons based on query parameters
    """
    location_name = request.query_params.get('location_name', None)
    # start with all beacons
    beacons = Beacons.objects.all()
    if location_name:
        beacons = Beacons.objects.filter(location_name__icontains=location_name)

    if not beacons.exists():
        return Response(
            {"message": "No beacons found matching the query."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the filtered beacons
    serializer = BeaconsSerializer(beacons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def active_beacons(request):
    """
    Retrieve a count of active beacons or a list of active beacons.
    """
    beacons = Beacons.objects.filter(status='Active')
    if not beacons.exists():
        return Response({"message", "No active beacons found"}, status=404)

    # count active beacons
    count = beacons.count()
    return Response({"count": count, "message": f"Found {count} active beacons."}, status=200)


@api_view(['GET'])
def beacons_count(request):
    """
    counts the total beacons
    """
    total_beacons = Beacons.objects.count()
    if not total_beacons:
        return Response({'message': 'No beacon found'}, status=404)
    return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=200)