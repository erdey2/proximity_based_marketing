from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserResponseSerializer  # Import the custom response serializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class UserListView(generics.ListCreateAPIView):
    """ API view to retrieve a list of users or create a new user. """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        tags=['Users'],
        summary="Retrieve a list of users",
        description="Returns a paginated list of all users in the system.",
        responses={200: UserResponseSerializer(many=True)},  # Use the custom response serializer
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Users"],
        summary="Create a New User",
        description="Creates a new user and returns access and refresh tokens.",
        request=UserSerializer,
        responses={
            201: UserResponseSerializer,  # Use the custom response serializer here
            400: {"description": "Bad Request"},
        },
    )
    def post(self, request, *args, **kwargs):
        # Validate and save user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return response with user data and JWT tokens
        return Response({
            "user": UserResponseSerializer(user).data,  # Use the custom response serializer
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

