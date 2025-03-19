from rest_framework.viewsets import GenericViewSet

from .models import Beacon
from .serializers import BeaconLocationSerializer, BeaconSimpleSerializer, BeaconSerializer, BeaconStatusSerializer, BeaconDataUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView

class BeaconList(ListCreateAPIView):
    """List all beacons or create a new one."""
    serializer_class = BeaconSerializer

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
        summary="Retrieve a list of beacons",
        description="Fetch all beacons with optional filtering by name and location name.",
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="Filter by beacon name (case-insensitive).",
                required=False
            ),
            OpenApiParameter(
                name="location_name",
                type=str,
                description="Filter by location name (case-insensitive).",
                required=False
            ),
        ],
        responses={200: BeaconSerializer(many=True)}
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
        request=BeaconSimpleSerializer,
        responses={
            201: BeaconSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BeaconDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a beacon."""
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer

    @extend_schema(
        summary="Retrieve a Beacon",
        description="Fetches the details of a specific beacon using its ID.",
        responses={
            200: BeaconSerializer,
            404: {"description": "Beacon not found."},
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Beacon",
        description="Updates an existing beacon name and/or location name.",
        request=BeaconSimpleSerializer,
        responses={
            200: BeaconSerializer,
            400: {"description": "Invalid data provided."},
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Beacon status from data received from mobile app",
        description="Updates an existing beacon (only the provided fields).",
        request=BeaconDataUpdateSerializer,
        responses={
            200: BeaconSerializer,
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
    serializer_class = BeaconSerializer

    def get_queryset(self):
        """Dynamically filter active beacons."""
        return Beacon.objects.filter(status__iexact='Active')  # Case-insensitive filtering

    @extend_schema(
        summary="Retrieve Active Beacons",
        description="Fetch a list of all beacons that are currently active. "
                    "This endpoint returns only beacons with a status of 'Active'.",
        responses={200: BeaconSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BeaconLocationList(ListAPIView):
    """Retrieve all beacons with their latitude and longitude."""
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


class BeaconStatus(RetrieveUpdateAPIView):
    """API to get and update beacon status"""
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer
    http_method_names = ['get', 'patch']

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
    def patch(self, request, pk):
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
