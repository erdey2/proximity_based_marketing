from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from rest_framework.response import Response
from campaign.models import Advertisements
from campaign.serializers import AdvertisementsSerializer
from django.utils.timezone import now
import uuid
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter


class AdvertisementRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Custom throttle rate for this view


@extend_schema(
    summary="Retrieve All Advertisements or Create a New One",
    description="""
     - **GET**: Retrieve a list of all advertisements.
     - **POST**: Create a new advertisement.
     """,
    request=AdvertisementsSerializer,  # Schema for POST request body
    responses={
        200: AdvertisementsSerializer(many=True),
        201: AdvertisementsSerializer,
        400: {"error": "Invalid data provided."},
    },
)
@throttle_classes([AdvertisementRateThrottle, AnonRateThrottle])
@api_view(['GET', 'POST'])
def advertisements_list(request):
    """
    List all advertisements or create a new one.

    **Methods:**
    - `GET`: Returns a list of all advertisements.
    - `POST`: Creates a new advertisement.

    **Responses:**
    - `200 OK`: Returns a list of advertisements.
    - `201 Created`: Successfully created a new advertisement.
    - `400 Bad Request`: Invalid input data.
    """
    if request.method == 'GET':
        advertisements = Advertisements.objects.all()
        serializer = AdvertisementsSerializer(advertisements, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AdvertisementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Retrieve, Update, or Delete an Advertisement",
    description="""
        - **GET**: Retrieve details of a specific advertisement.
        - **PUT**: Update an existing advertisement (partial update supported).
        - **DELETE**: Remove an advertisement from the database.
    """,
    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the advertisement to retrieve, update, or delete."
        ),
    ],
    responses={
        200: AdvertisementsSerializer,
        204: {"message": "No Content (advertisement deleted)."},
        400: {"error": "Bad request, invalid data provided."},
        404: {"error": "Advertisement not found."},
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
def advertisements_detail(request, pk):
    """
        Retrieve, update, or delete an advertisement item.

        **Methods:**
        - `GET`: Fetch details of an advertisement by ID.
        - `PUT`: Update advertisement fields (partial updates allowed).
        - `DELETE`: Remove the advertisement.

        **Parameters:**
        - `pk` (int): The primary key of the advertisement.

        **Responses:**
        - `200 OK`: Returns the advertisement details.
        - `400 Bad Request`: Invalid input data.
        - `404 Not Found`: If the advertisement does not exist.
        - `204 No Content`: Advertisement deleted successfully.
        """
    try:
        advertisement = Advertisements.objects.get(pk=pk)
    except Advertisements.DoesNotExist:
        return Response({"error": "Advertisement not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdvertisementsSerializer(advertisement)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AdvertisementsSerializer(advertisement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        advertisement.delete()
        return Response(status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary="Search Advertisements",
    description="Search for advertisements based on the title. If a title is provided as a query parameter, it returns matching advertisements; otherwise, it returns all advertisements.",
    parameters=[
        OpenApiParameter(
            name="title",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter advertisements by title (case-insensitive match)."
        )
    ],
    responses={
        200: AdvertisementsSerializer(many=True),
        404: {"message": "No advertisements found matching the query."},
    },
)
@api_view(['GET'])
def advertisements_search(request):
    """
        Search for advertisements based on query parameters (title).

        Query Parameters:
        - `title` (optional): Case-insensitive partial match on advertisement titles.

        Responses:
        - 200: Returns a list of advertisements matching the query.
        - 404: No advertisements found.
        """
    title = request.query_params.get('title', None)
    # start with all advertisements
    advertisements = Advertisements.objects.all()
    if title:
        advertisements = Advertisements.objects.filter(title__icontains=title)

    if not advertisements.exists():  # Check if the queryset is empty
        return Response({"message": "No advertisements found matching the query."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the filtered advertisements
    serializer = AdvertisementsSerializer(advertisements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Retrieve Active Advertisements",
    description="""
        This endpoint returns a list of advertisements that are currently active.

        **Logic:**
        - An advertisement is considered active if:
          - `start_date` is before or equal to the current time.
          - `end_date` is after or equal to the current time.

        **Example Use Case:**
        - If today's date is **Jan 29, 2025**, this API will return advertisements with:
          - `start_date` ≤ Jan 29, 2025
          - `end_date` ≥ Jan 29, 2025
    """,
    responses={
        200: AdvertisementsSerializer(many=True),
        404: {"message": "No active advertisements found."},
    },
)
@api_view(['GET'])
def advertisements_active(request):
    """
        List all active advertisements.

        **Method:**
        - `GET`: Fetches all advertisements that are currently active.

        **Logic:**
        - An advertisement is active if `start_date` is before or equal to the current time
          and `end_date` is after or equal to the current time.

        **Responses:**
        - `200 OK`: Returns a list of active advertisements.
        - `404 Not Found`: No active advertisements exist at the moment.
        """
    current_time = now()  # Get the current datetime
    advertisements = Advertisements.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    serializer = AdvertisementsSerializer(advertisements, many=True)
    return Response(serializer.data)
