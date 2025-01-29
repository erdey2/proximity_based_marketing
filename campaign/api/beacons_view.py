from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from campaign.models import Beacons
from campaign.serializers import BeaconsSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


class AllBeacons(ListAPIView):
    queryset = Beacons.objects.all()
    serializer_class = BeaconsSerializer

@extend_schema(
    summary="List or Create Beacons",
    description="""
        This endpoint allows users to **retrieve all beacons** or **create a new beacon**.

        **Methods:**
        - `GET`: Returns a list of all beacons in the system.
        - `POST`: Creates a new beacon with the provided data.

        **Example Use Case:**
        - A business owner wants to register new beacons in a proximity marketing system.
        - A user wants to fetch all available beacons for location-based advertisements.

        **Validation:**
        - Ensure that the `POST` request includes all required fields for beacon creation.
    """,
    responses={
        200: BeaconsSerializer(many=True),
        201: BeaconsSerializer,
        400: {"message": "Invalid data provided."},
    },

)
@api_view(['GET', 'POST'])
def beacons_list(request):
    """
    List all beacons or create a new one.

    **Methods:**
    - `GET`: Retrieves all registered beacons.
    - `POST`: Registers a new beacon.

    **Responses:**
    - `200 OK`: Returns a list of all beacons.
    - `201 Created`: Successfully created a new beacon.
    - `400 Bad Request`: Invalid data was provided.
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


@extend_schema(
    summary="Retrieve, Update, or Delete a Beacon",
    description="""
        This endpoint allows users to **retrieve**, **update**, or **delete** a beacon by its `beacon_id`.

        **Methods:**
        - `GET`: Fetches the details of a specific beacon.
        - `PUT`: Updates the information of a specific beacon.
        - `DELETE`: Removes a beacon from the system.

        **Example Use Case:**
        - A user wants to fetch beacon details for a specific location.
        - An admin wants to update beacon details (e.g., new location name).
        - A beacon that is no longer in use needs to be removed.

        **Validation:**
        - Ensure that the `beacon_id` exists before making an update or delete request.
    """,
    responses={
        200: BeaconsSerializer,
        204: {"message": "Beacon deleted successfully."},
        400: {"message": "Invalid data provided."},
        404: {"message": "Beacon not found."},
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
def beacons_detail(request, beacon_id):
    """
    Retrieve, update, or delete a beacon item.

    **Methods:**
    - `GET`: Retrieves details of a specific beacon.
    - `PUT`: Updates an existing beacon's information.
    - `DELETE`: Deletes a beacon.

    **Responses:**
    - `200 OK`: Returns beacon details.
    - `204 No Content`: Successfully deleted.
    - `400 Bad Request`: Invalid data provided.
    - `404 Not Found`: Beacon does not exist.
    """
    try:
        beacon = Beacons.objects.get(beacon_id=beacon_id)
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


@extend_schema(
    summary="Search Beacons by Location Name",
    description="""
        This endpoint allows users to search for beacons based on a location name query parameter.

        **Methods:**
        - `GET`: Retrieves a list of beacons that match the provided `location_name` query.

        **Example Use Case:**
        - A user wants to find beacons deployed in a specific mall or street.
        - A system admin wants to filter beacons by their location.

        **Validation:**
        - If no `location_name` is provided, all beacons are returned.
        - If no matching beacons are found, an appropriate response is returned.
    """,
    parameters=[
        OpenApiParameter(
            name="location_name",
            description="Filter beacons by partial or full location name",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: BeaconsSerializer(many=True),
        404: {"message": "No beacons found matching the query."},
    },
)
@api_view(['GET'])
def beacons_search(request):
    """
    Search for beacons based on query parameters (`location_name`).

    **Method:**
    - `GET`: Returns a list of beacons that match the search query.

    **Query Parameter:**
    - `location_name` (optional): Case-insensitive search for beacons by location.

    **Responses:**
    - `200 OK`: Returns a list of matching beacons.
    - `404 Not Found`: No beacons matched the search criteria.
    """
    location_name = request.query_params.get('location_name', None)
    # start with all beacons
    beacons = Beacons.objects.all()
    if location_name:
        beacons = Beacons.objects.filter(location_name__icontains=location_name)

    if not beacons.exists():
        return Response({"message": "No beacons found matching the query."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the filtered beacons
    serializer = BeaconsSerializer(beacons, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Retrieve Active Beacons Count",
    description="""
       This endpoint allows authenticated users to retrieve the count of active beacons.

       **Methods:**
       - `GET`: Returns the total number of active beacons.

       **Example Use Case:**
       - A system admin wants to monitor active beacons in a given area.
       - A user needs to confirm whether active beacons are available.

       **Validation:**
       - Authentication is required (`IsAuthenticated`).
       - If no active beacons are found, an appropriate response is returned.
   """,
    responses={
        200: {
            "count": "integer (number of active beacons)",
            "message": "string (description of active beacons count)"
        },
        404: {"message": "No active beacons found"},
        401: {"detail": "Authentication credentials were not provided."}
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_beacons(request):
    """
    Retrieve a count of active beacons.

    **Method:**
    - `GET`: Returns the total number of active beacons.

    **Authentication:**
    - User must be authenticated.

    **Responses:**
    - `200 OK`: Returns a count of active beacons.
    - `404 Not Found`: No active beacons available.
    - `401 Unauthorized`: User is not authenticated.
    """
    beacons = Beacons.objects.filter(status='Active')
    if not beacons.exists():
        return Response({"message", "No active beacons found"}, status=404)

    # count active beacons
    count = beacons.count()
    return Response({"count": count, "message": f"Found {count} active beacons."}, status=200)


@extend_schema(
    summary="Retrieve Total Beacon Count",
    description="""
        This endpoint returns the total number of beacons in the system.

        **Methods:**
        - `GET`: Fetch the total count of all beacons.

        **Example Use Case:**
        - A system admin wants to track the total number of registered beacons.
        - A dashboard displays the total number of beacons for analytics.

        **Responses:**
        - `200 OK`: Returns the total beacon count.
        - `404 Not Found`: No beacons are available.
    """,
    responses={
        200: {
            "count": "integer (total number of beacons)",
            "message": "string (description of beacon count)"
        },
        404: {"message": "No beacon found"}
    },

)
@api_view(['GET'])
def beacons_count(request):
    """
    Retrieve the total count of beacons.

    **Method:**
    - `GET`: Returns the total count of all beacons.

    **Responses:**
    - `200 OK`: Returns a count of total beacons.
    - `404 Not Found`: No beacons available.
    """
    total_beacons = Beacons.objects.count()
    if not total_beacons:
        return Response({'message': 'No beacon found'}, status=404)
    return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=200)


@extend_schema(
    summary="Receive Beacon Data",
    description="""
        This endpoint receives data from a mobile app about a beacon's ID, battery status, and signal strength (RSSI).

        **Methods:**
        - `POST`: Receives beacon data from a mobile application.

        **Example Use Case:**
        - A mobile app collects beacon data (e.g., battery status, signal strength) and sends it to the server.
        - This can be used for monitoring beacon health, performance, and real-time data.

        **Request Body:**
        - `beacon_id`: string (unique identifier of the beacon)
        - `battery_status`: integer (percentage battery remaining)
        - `rssi`: integer (signal strength of the beacon)

        **Responses:**
        - `201 Created`: Successfully saved beacon data.
        - `400 Bad Request`: Missing required fields in the request.
        - `500 Internal Server Error`: Server error during processing.
    """,
    request={
        "beacon_id": "string",
        "battery_status": "integer",
        "rssi": "integer"
    },
    responses={
        201: {
            "message": "Beacon data received successfully",
            "data": "BeaconsSerializer"
        },
        400: {
            "error": "Missing required fields (beacon_id, battery_status, rssi)"
        },
        500: {
            "error": "Internal server error message"
        }
    },
)
@api_view(['POST'])
def beacons_info(request):
    """
    Receive beacon data from the mobile app.

    **Method:**
    - `POST`: Receives the beacon's unique ID, battery status, and signal strength (RSSI) from a mobile application.

    **Request Body:**
    - `beacon_id`: string (Unique identifier of the beacon)
    - `battery_status`: integer (Battery percentage)
    - `rssi`: integer (Signal strength)

    **Responses:**
    - `201 Created`: Successfully saves the beacon data.
    - `400 Bad Request`: Missing required fields.
    - `500 Internal Server Error`: General error if something goes wrong.
    """
    try:
        beacon_id = request.data.get('beacon_id')  # Unique ID of the beacon
        battery_status = request.data.get('battery_status')  # Battery percentage
        rssi = request.data.get('rssi')  # Signal strength

        if not beacon_id or battery_status is None or rssi is None:
            return Response({"error": "Missing required fields (ssid, battery_status, rssi)"}, status=status.HTTP_400_BAD_REQUEST )
        # Save data to the database
        beacon_data = Beacons.objects.create(beacon_id=beacon_id, battery_status=battery_status, rssi=rssi)

        # Serialize the data for response
        serializer = BeaconsSerializer(beacon_data)

        return Response({"message": "Beacon data received successfully", "data": serializer.data}, status=status.HTTP_201_CREATED )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
