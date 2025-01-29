from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from campaign.models import AdvertisementsLog
from campaign.serializers import AdvertisementsLogsSerializer
from django.utils.timezone import now, timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    summary="List all advertisement logs or create a new one",
    description="""
        This endpoint provides two functionalities:
        1. **GET**: Retrieve a list of all advertisement logs.
        2. **POST**: Create a new advertisement log.

        **GET**:
        - Returns a list of all advertisement logs stored in the system.

        **POST**:
        - Receives advertisement log data and saves it in the database.

        **Request Body for POST**:
        - Logs include details such as `advertisement_id`, `user_id`, `timestamp`, and other necessary fields.

        **Responses**:
        - `200 OK`: Successfully retrieved advertisement logs.
        - `201 Created`: Successfully created a new advertisement log.
        - `400 Bad Request`: Data validation failed.
    """,
    request={
        "advertisement_id": "integer",
        "user_id": "integer",
        "timestamp": "datetime",
        # Add other fields specific to the AdvertisementLog model
    },
    responses={
        200: {
            "message": "List of advertisement logs",
            "data": "AdvertisementsLogsSerializer"
        },
        201: {
            "message": "Advertisement log created successfully",
            "data": "AdvertisementsLogsSerializer"
        },
        400: {
            "error": "Bad request: Validation failed"
        }
    },
)
@api_view(['GET', 'POST'])
def log_list(request):
    """
    List all advertisement logs or create a new one.

    **Method:**
    - `GET`: Retrieves all advertisement logs.
    - `POST`: Creates a new advertisement log.

    **Request Body for POST**:
    - `advertisement_id`: integer (ID of the advertisement)
    - `user_id`: integer (ID of the user interacting with the advertisement)
    - `timestamp`: datetime (time of interaction with the advertisement)

    **Responses**:
    - `200 OK`: Successfully retrieved the list of logs.
    - `201 Created`: Successfully created a new log entry.
    - `400 Bad Request`: Data validation errors for POST requests.
    """
    if request.method == 'GET':
        logs = AdvertisementsLog.objects.all()
        serializers = AdvertisementsLogsSerializer(logs, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = AdvertisementsLogsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Count advertisement logs for the past 24 hours",
    description="""
        This endpoint counts the number of advertisement logs created in the past 24 hours.
        - **GET**: Retrieves the count of advertisement logs for the past 24 hours.

        **Responses**:
        - `200 OK`: Successfully retrieved the count of advertisement logs in the past 24 hours.
        - `404 Not Found`: No advertisement logs found for the past 24 hours.
    """,
    responses={
        200: {
            "message": "Advertisement log count for the past 24 hours",
            "count": "integer"
        },
        404: {
            "message": "No advertisement logs found for the past 24 hours"
        }
    },
)
@api_view(['GET'])
def log_count(request):
    """
    Count advertisement logs for the past 24 hours.

    **Method:**
    - `GET`: Retrieves the count of advertisement logs from the past 24 hours.

    **Responses**:
    - `200 OK`: Successfully retrieved the count of advertisement logs for the past 24 hours.
    - `404 Not Found`: No advertisement logs found for the past 24 hours.
    """
    start_date = now() - timedelta(days=1)
    recent_advertisements = AdvertisementsLog.objects.filter(timestamp__gte=start_date).count()
    if not recent_advertisements:
        return Response({'message': 'No ads found'}, status=404)
    return Response({"count": recent_advertisements, "message": f"Found {recent_advertisements} ads."}, status=200)

