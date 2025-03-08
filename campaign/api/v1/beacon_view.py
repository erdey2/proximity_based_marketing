from campaign.models import Beacon
from campaign.serializers import BeaconSerializer, BeaconLocationSerializer, BeaconSimpleSerializer, BeaconListSerializer, BeaconStatusSerializer, BeaconPartialUpdateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter,OpenApiResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination

class BeaconPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 50

class BeaconList(ListCreateAPIView):
        """List all beacons or create a new one."""
        serializer_class = BeaconListSerializer
        pagination_class = BeaconPagination

        def get_queryset(self):
            qs = Beacon.objects.all()
            name = self.request.GET.get('name')
            location_name = self.request.GET.get('location_name')
            if name:
                qs = qs.filter(name__icontains=name)
            if location_name:
                qs = qs.filter(location_name__icontains=location_name)
            return qs

        @extend_schema(
            summary="Retrieve Beacons",
            description="""
                Retrieves a **paginated list** of beacons with optional filters:
                **Filter Parameters:**
                - `name` (string, optional): Search for beacons by name.
                - `location_name` (string, optional): Filter beacons by location.
                
                **Example Requests:**
                ``` GET /api/beacons/?name=beacon1&location_name=Jemo ```
                **Responses:**
                - `200 OK`: Returns a paginated list of beacons.
                - `400 Bad Request`: If an invalid filter is provided.
                """,
            parameters=[
                OpenApiParameter(name="name", type=str, description="Filter by beacon name", required=False),
                OpenApiParameter(name="location_name", type=str, description="Filter by location name", required=False),
            ],
            responses={
                200: BeaconListSerializer(many=True),
                400: OpenApiResponse(description="Invalid input data"),
            },
        )
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        @extend_schema(
            summary="Create a New Beacon",
            description="""
                Creates a **new beacon** with the required data.
                
                **Required Fields:**
                - `name` (string): The beacon's name.
                - `location_name` (string): The location where the beacon is located.

                **Example Request Body:**
                ```json
                {
                    "name": "Beacon 1",
                    "location_name": "Jemo"
                }
                ```

                **Responses:**
                - `201 Created`: Successfully created a new beacon.
                - `400 Bad Request`: If validation fails.
                """,
            request=BeaconListSerializer,
            responses={
                201: BeaconListSerializer,
                400: OpenApiResponse(description="Invalid input data"),
            },
        )
        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

class BeaconDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a beacon."""
    queryset = Beacon.objects.all()
    serializer_class = BeaconPartialUpdateSerializer

    @extend_schema(
        summary="Retrieve a Beacon",
        description="Fetches the details of a specific beacon using its ID.",
        responses={
            200: BeaconListSerializer,
            404: {"description": "Beacon not found."},
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Beacon",
        description="Updates an existing beacon. Requires full object replacement.",
        request=BeaconSimpleSerializer,
        responses={
            200: BeaconListSerializer,
            400: {"description": "Invalid data provided."},
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update a Beacon",
        description="Partially updates an existing beacon (only the provided fields).",
        request=BeaconStatusSerializer,
        responses={
            200: BeaconListSerializer,
            400: {"description": "Invalid data provided."},
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Beacon",
        description="Deletes a beacon permanently from the system.",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BeaconActive(ListAPIView):
    """Retrieve a list of active beacons."""
    serializer_class = BeaconListSerializer

    def get_queryset(self):
        """Dynamically filter active beacons."""
        return Beacon.objects.filter(status__iexact='Active')  # Case-insensitive filtering

    @extend_schema(
        summary="Retrieve Active Beacons",
        description="""
            This endpoint allows authenticated users to retrieve the list of active beacons.

            **Methods:**
            - `GET`: Returns a list of active beacons.

            **Example Use Case:**
            - A system admin wants to monitor active beacons in a given area.
            - A user needs to confirm whether active beacons are available.

            **Validation:**
            - Authentication is required (`IsAuthenticated`).
            - If no active beacons are found, an empty list is returned.
            """,
        responses={
            200: BeaconListSerializer(many=True),
            401: {"detail": "Authentication credentials were not provided."}
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BeaconCount(APIView):
    """Retrieve the total count of beacons."""
    # permission_classes = [IsAuthenticated]  # Enforce authentication

    @extend_schema(
        summary="Retrieve Total Beacon Count",
        description="""
        This endpoint allows authenticated users to retrieve the total count of beacons in the system.

        **Methods:**
        - `GET`: Returns the total number of beacons.

        **Example Use Case:**
        - A system admin wants to monitor the number of beacons.

        **Validation:**
        - Authentication is required (`IsAuthenticated`).
        - If no beacons are found, an appropriate response is returned.
        """,
        responses={
            200: {
                "count": "integer (total number of beacons)",
                "message": "string (description of beacon count)"
            },
            204: {"message": "No beacons available."},
            401: {"detail": "Authentication credentials were not provided."}
        },
    )
    def get(self, request):
        total_beacons = Beacon.objects.count()
        if total_beacons == 0:
            return Response({'message': 'No beacons available.'}, status=status.HTTP_204_NO_CONTENT)

        return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=status.HTTP_200_OK)

class BeaconLocationList(ListAPIView):
    """Retrieve all beacons with their latitude and longitude."""
    pagination_class = BeaconPagination
    queryset = Beacon.objects.all()
    serializer_class = BeaconLocationSerializer

    @extend_schema(
        summary="Retrieve All Beacons' Locations",
        description="""
            Fetch a list of all beacons with their respective locations (latitude & longitude).

            **Example Response:**
            ```json
            [
                {
                    "beacon_id": 1,
                    "name": "Beacon 1",
                    "latitude": 9.031,
                    "longitude": 38.746
                },
                {
                    "beacon_id": 2,
                    "name": "Beacon 2",
                    "latitude": 9.035,
                    "longitude": 38.750
                }
            ]
            ```
        """,
        responses={200: BeaconLocationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BeaconLocationCount(APIView):
    """API endpoint to count the total number of unique beacon locations."""
    # permission_classes = [IsAuthenticated]  # Enforce authentication
    @extend_schema(
        summary="Get Total Unique Beacon Locations",
        description="Returns the total number of unique beacon locations in the system.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "total_locations": {
                        "type": "integer",
                        "example": 8
                    }
                }
            },
            204: {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "No beacon locations found"
                    }
                }
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided."
                    }
                }
            }
        }
    )
    def get(self, request):
        total_locations = Beacon.objects.exclude(location_name__isnull=True).values('location_name').distinct().count()

        if total_locations == 0:
            return Response({'message': 'No beacon locations found'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'total_locations': total_locations}, status=status.HTTP_200_OK)

class BeaconStatus(RetrieveUpdateAPIView):
    """API to get and update beacon status"""
    queryset = Beacon.objects.all()
    serializer_class = BeaconListSerializer
    # permission_classes = [IsAuthenticated]  # Enforce authentication

    @extend_schema(
        summary="Retrieve Beacon Status",
        description="Fetch the current active/inactive status of a beacon.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "beacon_id": {"type": "string", "example": "123ABC"},
                    "is_active": {"type": "boolean", "example": True}
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Beacon not found"}
                }
            }
        }
    )
    def get(self, request, pk):
        """Retrieve beacon status"""
        beacon = self.get_object()
        return Response({"beacon_id": str(beacon.beacon_id), "is_active": beacon.is_active()})

    @extend_schema(
        summary="Update Beacon Status",
        description="Change the beacon status (Active/Inactive).",
        request=BeaconStatusSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Beacon status updated to Active"},
                    "beacon_id": {"type": "string", "example": "123ABC"},
                    "is_active": {"type": "boolean", "example": True}
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Invalid status. Use 'Active' or 'Inactive'."}
                }
            }
        }
    )
    def put(self, request, pk):
        """Change the status of a beacon (Active/Inactive)"""
        beacon = self.get_object()
        serializer = self.get_serializer(beacon, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": f"Beacon status updated to {serializer.validated_data['status']}",
                    "beacon_id": str(beacon.beacon_id),
                    "is_active": beacon.is_active()
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




