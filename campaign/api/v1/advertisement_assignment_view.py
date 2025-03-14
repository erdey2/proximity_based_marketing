from campaign.models import Beacon, Advertisement, AdvertisementAssignment
from campaign.serializers import BeaconSerializer, AdvertisementAssignmentSerializer, AdvertisementWithBeaconsSerializer, AdvertisementAssignmentBeaconSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils.timezone import now

class AdvertisementAssignmentList(ListCreateAPIView):
    """API endpoint for listing and creating advertisement assignments."""
    serializer_class = AdvertisementAssignmentSerializer

    def get_queryset(self):
        qs = AdvertisementAssignment.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                qs = qs.filter(start_date__gte=parsed_start_date)
            except ValueError:
                return Advertisement.objects.none()  # Return empty queryset if date format is invalid

        if end_date:
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                qs = qs.filter(end_date__lte=parsed_end_date)
            except ValueError:
                return Advertisement.objects.none()
        return qs

    @extend_schema(
        summary="Retrieve Advertisement Assignments",
        description="""
            Retrieves a **paginated list** of advertisement assignments.

            **Responses:**
            - `200 OK`: Returns a paginated list of advertisement assignments.
            - `400 Bad Request`: If an invalid request is made.
        """,
        parameters=[
            OpenApiParameter(name="start_date", type=str, description="Filter by start date (YYYY-MM-DD)", required=False),
            OpenApiParameter(name="end_date", type=str, description="Filter by end date (YYYY-MM-DD)", required=False),
        ],
        responses={
            200: AdvertisementAssignmentSerializer(many=True),
            400: OpenApiResponse(description="Invalid request"),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Advertisement Assignment",
        description="""
            Assigns an advertisement to a specific beacon.

            **Required Fields:**
            - `advertisement` (integer): The ID of the advertisement.
            - `beacon` (integer): The ID of the beacon.

            **Example Request Body:**
            ```json
            {
                "advertisement": 1,
                "beacon": 2,
            }
            ```

            **Responses:**
            - `201 Created`: Successfully assigned the advertisement.
            - `400 Bad Request`: If validation fails.
        """,
        request=AdvertisementAssignmentSerializer,
        responses={
            201: AdvertisementAssignmentSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AdvertisementAssignmentDetail(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update, or delete an advertisement assignment by ID. """
    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer

    @extend_schema(
        summary="Retrieve Advertisement Assignment",
        description="""
            Fetch details of a specific **Advertisement Assignment** by its ID.

            **Example Request:**
            ```
            GET /api/advertisement-assignments/1/
            ```

            **Responses:**
            - `200 OK`: Successfully retrieved assignment details.
            - `404 Not Found`: If the assignment does not exist.
        """,
        responses={
            200: AdvertisementAssignmentSerializer,
            404: OpenApiResponse(description="Assignment not found"),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update Advertisement Assignment",
        description="""
            Fully update an **Advertisement Assignment** by its ID.

            **Required Fields:**
            - `advertisement` (integer): The advertisement ID.
            - `beacon` (integer): The beacon ID.

            **Example Request:**
            ```json
            {
                "advertisement": 1,
                "beacon": 5,
            }
            ```

            **Responses:**
            - `200 OK`: Successfully updated.
            - `400 Bad Request`: If validation fails.
            - `404 Not Found`: If the assignment does not exist.
        """,
        request=AdvertisementAssignmentSerializer,
        responses={
            200: AdvertisementAssignmentSerializer,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Assignment not found"),
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update Advertisement Assignment",
        description="""
            Partially update an **Advertisement Assignment** by ID.

            **Example Request:**
            ```json
            {
                "beacon": 3
            }
            ```

            **Responses:**
            - `200 OK`: Successfully updated.
            - `400 Bad Request`: If validation fails.
            - `404 Not Found`: If the assignment does not exist.
        """,
        request=AdvertisementAssignmentBeaconSerializer,
        responses={
            200: AdvertisementAssignmentSerializer,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Assignment not found"),
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete Advertisement Assignment",
        description="""
            Remove an **Advertisement Assignment** by its ID.

            **Responses:**
            - `204 No Content`: Successfully deleted.
            - `404 Not Found`: If the assignment does not exist.
        """,
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            404: OpenApiResponse(description="Assignment not found"),
        }

    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AdvertisementListWithBeaconsView(ListAPIView):
    """ API endpoint to list advertisements along with their assigned beacons. """
    queryset = Advertisement.objects.prefetch_related("advertisement_assignments__beacon").all()
    serializer_class = AdvertisementWithBeaconsSerializer

    @extend_schema(
        summary="List Advertisements with Assigned Beacons",
        description="""
            Retrieves a **paginated list** of advertisements along with their assigned beacons.

            Each advertisement will include a list of associated beacons (including their locations).

            **Example Request:**
            ```
            GET /api/advertisements-with-beacons/
            ```

            **Responses:**
            - `200 OK`: Returns a paginated list of advertisements with assigned beacons.
        """,
        responses={
            200: AdvertisementWithBeaconsSerializer(many=True),
            400: OpenApiResponse(description="Invalid request"),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AdvertisementActive(ListAPIView):
    """List all active advertisements."""
    serializer_class = AdvertisementAssignmentSerializer

    def get_queryset(self):
        """Return only active advertisements based on start and end dates."""
        current_time = now()
        return Advertisement.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

    @extend_schema(
        summary="Get active advertisements",
        description="""
            Fetch all advertisements that are currently active based on their start and end dates.

            **Example Request:**
            ```
            GET /api/advertisements/active/
            ```

            **Responses:**
            - `200 OK`: Returns a list of active advertisements.
            - `404 Not Found`: If no active advertisements are available.
        """,
        responses={
            200: AdvertisementAssignmentSerializer(many=True),
            404: OpenApiResponse(description="No active advertisements found")
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No active advertisements found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BeaconListWithAdsView(ListAPIView):
    """ API endpoint to list beacons along with their assigned advertisements."""
    queryset = Beacon.objects.prefetch_related("advertisement_assignments__advertisement").all()
    serializer_class = BeaconSerializer

    @extend_schema(
        summary="List Beacons with Assigned Advertisements",
        description="""
            Retrieves a **paginated list** of beacons along with their assigned advertisements.

            Each beacon will include a list of advertisements it is linked to.

            **Example Request:**
            ```
            GET /api/beacons-with-ads/
            ```

            **Responses:**
            - `200 OK`: Returns a paginated list of beacons with assigned advertisements.
            - `400 Bad Request`: If the request is invalid.
        """,
        responses={
            200: BeaconSerializer(many=True),
            400: OpenApiResponse(description="Invalid request"),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
