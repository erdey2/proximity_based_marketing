from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from campaign.models import AdvertisementLog
from campaign.serializers import AdvertisementLogSerializer
from django.utils.timezone import now, timedelta
from drf_spectacular.utils import extend_schema


class LogList(APIView):
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
    @extend_schema(
        summary="Retrieve Advertisement Logs",
        description="Fetches a list of all advertisement logs stored in the system.",
        responses={200: AdvertisementLogSerializer(many=True)}
    )
    def get(self, request):
        logs = AdvertisementLog.objects.all()
        serializers = AdvertisementLogSerializer(logs, many=True)
        return Response(serializers.data)

    @extend_schema(
        summary="Create a New Advertisement Log",
        description="""
            Creates a new advertisement log entry.

            **Required Fields**:
            - `advertisement_id` (integer): The ID of the advertisement being logged.
            - `user_id` (integer): The ID of the user who interacted with the advertisement.
            - `timestamp` (datetime): The time of interaction.

            **Responses**:
            - `201 Created`: Log entry created successfully.
            - `400 Bad Request`: Validation errors.
            """,
        request=AdvertisementLogSerializer,
        responses={
            201: AdvertisementLogSerializer,
            400: {"message": "Invalid input data."},
        }
    )
    def post(self, request):
        serializer = AdvertisementLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LogsCount(APIView):
    """
        Count advertisement logs for the past 24 hours.

        **Method:**
        - `GET`: Retrieves the count of advertisement logs from the past 24 hours.

        **Responses**:
        - `200 OK`: Successfully retrieved the count of advertisement logs for the past 24 hours.
        - `404 Not Found`: No advertisement logs found for the past 24 hours.
    """
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
    def get(self, request):
        start_date = now() - timedelta(days=1)
        recent_advertisements = AdvertisementLog.objects.filter(timestamp__gte=start_date).count()
        if not recent_advertisements:
            return Response({'message': 'No ads found'}, status=404)
        return Response({"count": recent_advertisements, "message": f"Found {recent_advertisements} ads."}, status=200)



