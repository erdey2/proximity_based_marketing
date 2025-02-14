from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from campaign.models import Beacon
from campaign.serializers import BeaconSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404

class BeaconList(APIView):
    """List all beacons or create a new one. """
    @extend_schema(
        summary="Retrieve All Beacons",
        description="Fetches a list of all registered beacons in the system.",
        responses={200: BeaconSerializer(many=True)}
    )
    def get(self, request):
        beacons = Beacon.objects.all()
        serializer = BeaconSerializer(beacons, many=True)
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
        request=BeaconSerializer,
        responses={
            201: BeaconSerializer,
            400: {"message": "Invalid input data."},
        }
    )
    def post(self, request):
        serializer = BeaconSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class BeaconDetail(APIView):
    """Retrieve, update, or delete a beacon item. """
    @extend_schema(
        summary="Retrieve a Beacon",
        description="Fetches the details of a specific beacon using its `beacon_id`.",
        responses={
            200: BeaconSerializer,
            404: {"message": "Beacon not found."},
        },
        parameters=[
            OpenApiParameter(name="beacon_id", description="ID of the beacon", required=True, type=int),
        ]
    )
    def get(self, request, pk):
        try:
            beacon = Beacon.objects.get(pk=pk)
            serializer = BeaconSerializer(beacon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Beacon.DoesNotExist:
            return Response({"message": "Beacon not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a Beacon",
        description="Updates a beacon's details using `beacon_id`. Partial updates are allowed.",
        request=BeaconSerializer,
        responses={
            200: BeaconSerializer,
            400: {"message": "Invalid data provided."},
            404: {"message": "Beacon not found."},
        },
    )
    def put(self, request, pk):
        try:
            beacon = Beacon.objects.get(pk=pk)
            serializer = BeaconSerializer(beacon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Beacon.DoesNotExist:
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
            beacon = Beacon.objects.get(pk=pk)
            beacon.delete()
            return Response({"message": "Beacon deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Beacon.DoesNotExist:
            return Response({"message": "Beacon not found."}, status=status.HTTP_404_NOT_FOUND)

class BeaconsSearch(APIView):
    """Search for beacons based on query parameters (`location_name`). """
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
            200: BeaconSerializer(many=True),
            404: {"message": "No beacons found matching the query."},
        },
    )
    def get(self, request):
        location_name = request.query_params.get('location_name', None)
        # start with all beacons
        beacons = Beacon.objects.all()
        if location_name:
            beacons = Beacon.objects.filter(location_name__icontains=location_name)

            if not beacons.exists():
                return Response({"message": "No beacons found matching the query."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the filtered beacons
            serializer = BeaconSerializer(beacons, many=True)
            return Response(serializer.data)


class BeaconActive(APIView):
    """Retrieve a count of active beacons. """
    
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
        beacons = Beacon.objects.filter(status='Active')
        if not beacons.exists():
            return Response({"message", "No active beacons found"}, status=404)

        # count active beacons
        count = beacons.count()
        return Response({"count": count, "message": f"Found {count} active beacons."}, status=200)

class BeaconCount(APIView):
    """Retrieve the total count of beacons. """
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
        total_beacons = Beacon.objects.count()
        if not total_beacons:
            return Response({'message': 'No beacon found'}, status=404)
        return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=200)

class BeaconLocationCount(APIView):
    """API endpoint to count the total number of unique beacon locations. """
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
        total_locations = Beacon.objects.values('location_name').distinct().count()
        return Response({'Total Locations': total_locations})


class BeaconInfoUpdate(APIView):
    """Receive beacon data from the mobile app. """
    @extend_schema(
        summary="Receive Beacon Data",
        description="""This endpoint receives data from a mobile app about a beacon's ID, battery status, and signal strength (RSSI).""",
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
    def put(self, request, pk):
        """ Update specific details of a beacon """
        beacon = get_object_or_404(Beacon, pk=pk)
        # Use BeaconsSerializer to validate and update beacon data
        serializer = BeaconSerializer(beacon, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Save the updated data to the database
            return Response({"message": "Beacon updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BeaconStatus(APIView):
    """ API to get and update beacon status"""

    def get(self, request, pk):
        """ Get the current status of the beacon """
        beacon = get_object_or_404(Beacon, pk=pk)
        return Response({"beacon_id": str(beacon.beacon_id), "is_active": beacon.is_active() } )

    def put(self, request, pk):
        """ Change the status of a beacon (Active/Inactive) """
        beacon = get_object_or_404(Beacon, pk=pk)
        new_status = request.data.get("status")  # Extract the new status from request

        if new_status not in [Beacon.Status.ACTIVE, Beacon.Status.INACTIVE]:
            return Response({"error": "Invalid status. Use 'Active' or 'Inactive'."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the model's change_status method
        beacon.change_status(new_status)

        return Response(
            {
                "message": f"Beacon status updated to {new_status}",
                "beacon_id": str(beacon.beacon_id),
                "is_active": beacon.is_active()
            },
            status=status.HTTP_200_OK)





