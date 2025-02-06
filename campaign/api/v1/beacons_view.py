from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from campaign.models import Beacons
from campaign.serializers import BeaconsSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class BeaconsList(APIView):
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
    @extend_schema(
        summary="Retrieve All Beacons",
        description="Fetches a list of all registered beacons in the system.",
        responses={200: BeaconsSerializer(many=True)}
    )
    def get(self, request):
        beacons = Beacons.objects.all()
        serializer = BeaconsSerializer(beacons, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Register a New Beacon",
        description="""
            Registers a new beacon with the provided data.

            **Required Fields**:
            - `beacon_id` (string): Unique identifier for the beacon.
            - 'name' (string): Unique name for beacon.
            - `location` (string): Description of the beacon's location.
            - `status` (string): Status of the beacon (e.g., active, inactive).

            **Responses**:
            - `201 Created`: Successfully created a new beacon.
            - `400 Bad Request`: Validation errors.
            """,
        request=BeaconsSerializer,
        responses={
            201: BeaconsSerializer,
            400: {"message": "Invalid input data."},
        }
    )
    def post(self, request):
        serializer = BeaconsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class BeaconsDetail(APIView):
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

    @extend_schema(
        summary="Retrieve a Beacon",
        description="Fetches the details of a specific beacon using its `beacon_id`.",
        responses={
            200: BeaconsSerializer,
            404: {"message": "Beacon not found."},
        },
        parameters=[
            OpenApiParameter(name="beacon_id", description="ID of the beacon", required=True, type=int),
        ]

    )
    def get(self, request, beacon_id):
        try:
            beacon = Beacons.objects.get(beacon_id=beacon_id)
            serializer = BeaconsSerializer(beacon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Beacons.DoesNotExist:
            return Response({"message": "Beacon not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a Beacon",
        description="Updates a beacon's details using `beacon_id`. Partial updates are allowed.",
        request=BeaconsSerializer,
        responses={
            200: BeaconsSerializer,
            400: {"message": "Invalid data provided."},
            404: {"message": "Beacon not found."},
        },
    )
    def put(self, request, pk):
        try:
            beacon = Beacons.objects.get(pk=pk)
            serializer = BeaconsSerializer(beacon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Beacons.DoesNotExist:
            return Response({"message": "Beacon not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a Beacon",
        description="Deletes a beacon using `beacon_id`.",
        responses={
            204: {"message": "Beacon deleted successfully."},
            404: {"message": "Beacon not found."},
        },
    )
    def delete(self, request, pk):
        try:
            beacon = Beacons.objects.get(pk=pk)
            beacon.delete()
            return Response({"message": "Beacon deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Beacons.DoesNotExist:
            return Response({"message": "Beacon not found."}, status=status.HTTP_404_NOT_FOUND)


class BeaconsSearch(APIView):
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
    @extend_schema(
        summary="Search Beacons by Location Name",
        description="""
            This endpoint allows users to search for beacons based on a location name query parameter.

            **Methods:**
            - `GET`: Retrieves a list of beacons that match the provided `location_name` query.

            **Example Use Case:**
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
    def get(self, request):
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


class BeaconsActive(APIView):
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
    
    #@permission_classes([IsAuthenticated])
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
    def get(self, request):
        beacons = Beacons.objects.filter(status='Active')
        if not beacons.exists():
            return Response({"message", "No active beacons found"}, status=404)

        # count active beacons
        count = beacons.count()
        return Response({"count": count, "message": f"Found {count} active beacons."}, status=200)

class BeaconsCount(APIView):
    """
    Retrieve the total count of beacons.

    **Method:**
    - `GET`: Returns the total count of all beacons.

    **Responses:**
    - `200 OK`: Returns a count of total beacons.
    - `404 Not Found`: No beacons available.
    """
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
    def get(self, request):
        total_beacons = Beacons.objects.count()
        if not total_beacons:
            return Response({'message': 'No beacon found'}, status=404)
        return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=200)

class BeaconsLocationsCount(APIView):
    """
    API endpoint to count the total number of unique beacon locations.

    Returns:
        - 200 OK: A JSON object containing the total count of unique locations.
        - 500 Internal Server Error: If a database error occurs.
    """
    @extend_schema(
        summary="Get Total Unique Beacon Locations",
        description="Returns the total number of unique beacon locations.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "Total Locations": {
                        "type": "integer",
                        "example": 8
                    }
                }
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Internal Server Error"
                    }
                }
            }
        }
    )
    def get(self, request):
        total_locations = Beacons.objects.values('location_name').distinct().count()
        return Response({'Total Locations': total_locations})


class BeaconsInfo(APIView):
    """
     Receive beacon data from the mobile app.

     **Method:**
     - `POST`: Receives the beacon's unique ID, battery status, and signal strength (RSSI) from a mobile application.

     **Request Body:**
     - `beacon_id`: string (Unique identifier of the beacon)
     - `battery_status`: float (Battery percentage)
     - `rssi`: float (Signal strength)

     **Responses:**
     - `201 Created`: Successfully saves the beacon data.
     - `400 Bad Request`: Missing required fields.
     - `500 Internal Server Error`: General error if something goes wrong.
     """
    @extend_schema(
        summary="Receive Beacon Data",
        description="""
        This endpoint receives data from a mobile app about a beacon's ID, battery status, and signal strength (RSSI).

        **Methods:**
        - `PUT`: Receives beacon data from a mobile application.

        **Example Use Case:**
        - A mobile app collects beacon data (e.g., battery status, signal strength) and sends it to the server.
        - This can be used for monitoring beacon health, performance, and real-time data.

        **Request Body:**
        - `beacon_id`: string (unique identifier of the beacon)
        - `battery_status`: float (percentage battery remaining)
        - `signal_strength`: float (signal strength of the beacon)

        **Responses:**
        - `201 Created`: Successfully saved beacon data.
        - `400 Bad Request`: Missing required fields in the request.
        - `500 Internal Server Error`: Server error during processing.
        """,
        request={
            "beacon_id": "string",
            "battery_status": "float",
            "signal_strength": "float"
        },
        responses={
            201: {
                "message": "Beacon data received successfully",
                "data": "BeaconsSerializer"
            },
            400: {
                "error": "Missing required fields (beacon_id, battery_status, signal_strength)"
            },
            500: {
                "error": "Internal server error message"
            }
        },
    )
    def put(self, request):
        try:
            beacon_id = request.data.get('beacon_id')  # Unique ID of the beacon
            battery_status = request.data.get('battery_status')  # Battery percentage
            signal_strength = request.data.get('signal_strength')  # Signal strength

            if not beacon_id or battery_status is None or signal_strength is None:
                return Response({"error": "Missing required fields (beacon_id, battery_status, signal_strength)"},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                beacon = Beacons.objects.get(beacon_id=beacon_id)
                beacon.battery_status = battery_status
                beacon.signal_strength = signal_strength
                beacon.save()
                return Response({"message": "Beacon data updated successfully"}, status=status.HTTP_200_OK)
            except Beacons.DoesNotExist:
                return Response({"error": "Beacon not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
