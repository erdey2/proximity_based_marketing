from beacons.models import Beacon
from advertisements.models import Advertisement
from assignments.models import AdvertisementAssignment
from .serializers import AdvertisementAssignmentSerializer, AdvertisementBeaconsSerializer, AdvertisementDateSerializer, BeaconAdvertisementsSerializer
from beacons.serializers import BeaconSerializer
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
        tags=["Assignments"],
        summary="Retrieve Advertisement Assignments",
        description="""
                Retrieves a **list of advertisement assignments** with optional date filters.

                **Filter Parameters:**
                - `start_date` (YYYY-MM-DD, optional): Filters assignments starting from this date.
                - `end_date` (YYYY-MM-DD, optional): Filters assignments ending before or on this date.

                **Example Requests:**
                ```
                GET /api/advertisement-assignments/?start_date=2024-03-01&end_date=2024-03-15
                ```

                **Responses:**
                - `200 OK`: Returns a paginated list of advertisement assignments.
                - `400 Bad Request`: If an invalid date format is provided.
            """,
        parameters=[
            OpenApiParameter(name="start_date", type=str, description="Filter by start date (YYYY-MM-DD)",
                             required=False),
            OpenApiParameter(name="end_date", type=str, description="Filter by end date (YYYY-MM-DD)", required=False),
        ],
        responses={
            200: AdvertisementAssignmentSerializer(many=True),
            400: OpenApiResponse(description="Invalid date format"),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Assignments"],
        summary="Create a New Advertisement Assignment",
        description="""
                Assign list of advertisements to a specific beacon or list of beacons to specific advertisement.

                **Required Fields:**
                - `advertisement` (integer): The advertisement being assigned.
                - `start_date` (YYYY-MM-DD): Start date of the assignment.
                - `end_date` (YYYY-MM-DD): End date of the assignment.
                - `assigned_to` (integer): The entity(beacon) assigned to the advertisement.

                **Example Request Body:**
                ```json
                {
                    "advertisement": 1,
                    "start_date": "2024-03-01",
                    "end_date": "2024-03-10",
                    "assigned_to": 5
                }
                ```

                **Responses:**
                - `201 Created`: Successfully created a new advertisement assignment.
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
        tags=["Assignments"],
        summary="Retrieve an Advertisement Assignment",
        description="""
                Fetches a **single advertisement assignment** by its ID.

                **Example Request:**
                ```
                GET /api/advertisement-assignments/1/
                ```

                **Responses:**
                - `200 OK`: Returns the advertisement assignment details.
                - `404 Not Found`: If the assignment does not exist.
            """,
        responses={
            200: AdvertisementAssignmentSerializer,
            404: OpenApiResponse(description="Advertisement assignment not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Assignments"],
        summary="Update an Advertisement Assignment",
        description="""
                Fully updates an **existing advertisement assignment**.

                **Example Request Body:**
                ```json
                {
                    "advertisement": 2,
                    "start_date": "2024-03-05",
                    "end_date": "2024-03-20",
                    "assigned_to": 7
                }
                ```

                **Responses:**
                - `200 OK`: Successfully updated the advertisement assignment.
                - `400 Bad Request`: If validation fails.
                - `404 Not Found`: If the assignment does not exist.
            """,
        request=AdvertisementAssignmentSerializer,
        responses={
            200: AdvertisementAssignmentSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Advertisement assignment not found"),
        },

    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=["Assignments"],
        summary="Partially Update an Advertisement Assignment",
        description="""
                Partially updates specific fields of an **existing advertisement assignment**.

                **Example Request Body:**
                ```json
                {
                    "end_date": "2024-03-25"
                }
                ```

                **Responses:**
                - `200 OK`: Successfully updated the advertisement assignment.
                - `400 Bad Request`: If validation fails.
                - `404 Not Found`: If the assignment does not exist.
            """,
        request=AdvertisementDateSerializer,
        responses={
            200: AdvertisementAssignmentSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Advertisement assignment not found"),
        },

    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Assignments"],
        summary="Delete an Advertisement Assignment",
        description="""
                Deletes an advertisement assignment by its ID.

                **Example Request:**
                ```
                DELETE /api/advertisement-assignments/1/
                ```

                **Responses:**
                - `204 No Content`: Successfully deleted the advertisement assignment.
                - `404 Not Found`: If the assignment does not exist.
            """,
        responses={
            204: OpenApiResponse(description="Successfully deleted"),
            404: OpenApiResponse(description="Advertisement assignment not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AdvertisementActive(ListAPIView):
    """List all active advertisements."""
    serializer_class = AdvertisementAssignmentSerializer

    def get_queryset(self):
        """Return only active advertisements based on start and end dates."""
        current_time = now()
        return Advertisement.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

    @extend_schema(
        tags=["Assignments"],
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

class AdvertisementBeaconsView(ListAPIView):
    """ API endpoint to list advertisement along with their assigned beacons. """
    queryset = Advertisement.objects.prefetch_related("advertisement_assignments__beacon").all()
    serializer_class = AdvertisementBeaconsSerializer

    @extend_schema(
        tags=["Assignments"],
        summary="List Advertisement with Assigned Beacons",
        description="""
            Retrieves a **list** of advertisement along with their assigned beacons.

            Each advertisement will include a list of associated beacons (including their locations).

            **Example Request:**
            ```
            GET /api/advertisement-beacons/
            ```

            **Responses:**
            - `200 OK`: Returns a paginated list of advertisements with assigned beacons.
        """,
        responses={
            200: AdvertisementBeaconsSerializer(many=True),
            400: OpenApiResponse(description="Invalid request"),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BeaconAdvertisementsView(ListAPIView):
    """ API endpoint to list beacons along with their assigned advertisements."""
    queryset = Beacon.objects.prefetch_related("advertisement_assignments__advertisement").all()
    serializer_class = BeaconAdvertisementsSerializer

    @extend_schema(
        tags=["Assignments"],
        summary="List Beacon with Assigned Advertisements",
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
            200: BeaconAdvertisementsSerializer(many=True),
            400: OpenApiResponse(description="Invalid request"),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

