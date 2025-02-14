from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from campaign.models import Advertisement
from campaign.serializers import AdvertisementSerializer
from django.utils.timezone import now
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404


class AdvertisementRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Custom throttle rate for this view

class AdvertisementsList(APIView):
    #@throttle_classes([AdvertisementRateThrottle, AnonRateThrottle])
    """
        List all advertisements or create a new one.
    """
    @extend_schema(
        summary="List All Advertisements",
        description="Fetches all advertisements available in the system.",
        responses={200: AdvertisementSerializer(many=True)}
    )
    def get(self, request):
        advertisements = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a New Advertisement",
        description="Creates a new advertisement in the system with provided details.",
        request=AdvertisementSerializer,
        responses={
            201: AdvertisementSerializer,
            400: {"message": "Invalid input data."},
        }
    )

    def post(self, request):
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AdvertisementDetail(APIView):
    """
    Retrieve, update, or delete an advertisement item.
    """

    @extend_schema(
        summary="Retrieve advertisement details",
        description="Fetches details of an advertisement by its primary key (ID).",
        responses={200: AdvertisementSerializer}
    )
    def get(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        serializer = AdvertisementSerializer(advertisement)
        return Response(serializer.data)

    @extend_schema(
        summary="Update an advertisement",
        description="Updates fields of an advertisement. Partial updates are allowed.",
        request=AdvertisementSerializer,
        responses={200: AdvertisementSerializer, 400: {"error": "Invalid input"}}
    )
    def put(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        serializer = AdvertisementSerializer(advertisement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete an advertisement",
        description="Deletes an advertisement by its primary key (ID).",
        responses={204: None, 404: {"error": "Advertisement not found"}}
    )
    def delete(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AdvertisementsSearch(APIView):
    """
    Search for advertisements based on query parameters (title).
    """

    @extend_schema(
        summary="Search advertisements",
        description="Search for advertisements by title using case-insensitive partial matching.",
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter advertisements by title (case-insensitive match)."
            )
        ],
        responses={200: AdvertisementSerializer(many=True), 404: {"message": "No advertisements found matching the query."}}
    )
    def get(self, request):
        title = request.query_params.get('title', None)
        advertisements = Advertisement.objects.all()

        if title:
            advertisements = advertisements.filter(title__icontains=title)

        if not advertisements.exists():  # Check if the queryset is empty
            return Response({"message": "No advertisements found matching the query."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered advertisements
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AdvertisementsActive(APIView):
    """
    List all active advertisements.
    """

    @extend_schema(
        summary="Get active advertisements",
        description="Fetch all advertisements that are currently active based on their start and end dates.",
        responses={200: AdvertisementSerializer(many=True), 404: {"message": "No active advertisements found."}}
    )
    def get(self, request):
        current_time = now()  # Get the current datetime
        advertisements = Advertisement.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

        if not advertisements.exists():
            return Response({"message": "No active advertisements found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)