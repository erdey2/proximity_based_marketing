from campaign.models import Beacon, Advertisement, AdvertisementAssignment
from campaign.serializers import BeaconSerializer, AdvertisementAssignmentSerializer, AdvertisementWithBeaconsSerializer, AdvertisementAssignmentBeaconSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

class AdvertisementAssignmentList(ListCreateAPIView):
    """API endpoint for listing and creating advertisement assignments."""
    queryset = AdvertisementAssignment.objects.all()
    serializer_class = AdvertisementAssignmentSerializer

    @extend_schema(
        summary="Retrieve Advertisement Assignments",
        description="""
            Retrieves a **paginated list** of advertisement assignments.

            **Responses:**
            - `200 OK`: Returns a paginated list of advertisement assignments.
            - `400 Bad Request`: If an invalid request is made.
        """,
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
