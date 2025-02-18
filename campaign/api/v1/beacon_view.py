from campaign.models import Beacon
from campaign.serializers import BeaconSerializer, BeaconStatusSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination

class BeaconPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 50

class BeaconList(ListCreateAPIView):
        """List all beacons or create a new one."""
        #queryset = Beacon.objects.all()
        serializer_class = BeaconSerializer

        # search based on beacon name, location_name etc
        """ filter_backends = [filters.SearchFilter]
        search_fields = ['name', 'location_name', 'status'] """

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
            summary="Retrieve All Beacons",
            description="Fetches a list of all registered beacons in the system.",
            responses={200: BeaconSerializer(many=True)}
        )
        def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)

        @extend_schema(
            summary="Register a New Beacon",
            request=BeaconSerializer,
            responses={201: BeaconSerializer, 400: {"message": "Invalid input data."}}
        )
        def post(self, request, *args, **kwargs):
            return super().post(request, *args, **kwargs)

class BeaconDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a beacon."""
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer

    @extend_schema(
        summary="Retrieve a Beacon",
        description="Fetches the details of a specific beacon using its ID.",
        parameters=[OpenApiParameter(name="pk", description="ID of the beacon", required=True, type=int)],
        responses={200: BeaconSerializer, 404: {"message": "Beacon not found."}}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Beacon",
        request=BeaconSerializer,
        responses={200: BeaconSerializer, 400: {"message": "Invalid data provided."}}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Beacon",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class BeaconActive(ListAPIView):
    """Retrieve a list of active beacons."""
    queryset = Beacon.objects.filter(status='Active')
    serializer_class = BeaconSerializer
    permission_classes = [IsAuthenticated]  # Ensure authentication if needed

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
            200: BeaconSerializer(many=True),
            401: {"detail": "Authentication credentials were not provided."}
        },
    )
    def get_queryset(self):
        """Override to ensure filtering of active beacons dynamically."""
        return Beacon.objects.filter(status='Active')

class BeaconCount(GenericAPIView):
    """Retrieve the total count of beacons."""
    permission_classes = [IsAuthenticated]  # Enforce authentication if needed

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
            404: {"message": "No beacon found"},
            401: {"detail": "Authentication credentials were not provided."}
        },
    )
    def get(self, request):
        total_beacons = Beacon.objects.count()
        if total_beacons == 0:
            return Response({'message': 'No beacon found'}, status=404)

        return Response({"count": total_beacons, "message": f"Found {total_beacons} beacons."}, status=200)

class BeaconLocationCount(GenericAPIView):
    """API endpoint to count the total number of unique beacon locations."""

    permission_classes = [IsAuthenticated]  # Enforce authentication (optional)

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
            404: {
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
        total_locations = Beacon.objects.values('location_name').distinct().count()

        if total_locations == 0:
            return Response({'message': 'No beacon locations found'}, status=404)

        return Response({'total_locations': total_locations}, status=200)

class BeaconInfoUpdate(UpdateAPIView):
    """Receive and update beacon data from the mobile app."""

    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer
    permission_classes = [IsAuthenticated]  # Enforce authentication

    @extend_schema(
        summary="Update Beacon Data",
        description="This endpoint updates a beacon's ID, battery status, and signal strength (RSSI).",
        request=BeaconSerializer,  # Properly referencing the serializer
        responses={
            200: BeaconSerializer,  # Returns updated data
            400: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Missing required fields (beacon_id, battery_status, signal_strength)"
                    }
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Beacon not found"
                    }
                }
            },
            500: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Internal server error message"
                    }
                }
            }
        },
    )
    def put(self, request, pk):
        """ Update specific details of a beacon """
        beacon = get_object_or_404(Beacon, pk=pk)

        serializer = self.get_serializer(beacon, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Beacon updated successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BeaconStatus(RetrieveUpdateAPIView):
    """API to get and update beacon status"""

    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer
    permission_classes = [IsAuthenticated]  # Enforce authentication

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





