from django.contrib.auth import get_user_model, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserResponseSerializer, LoginSerializer, LoginSuccessResponseSerializer
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework.views import APIView

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

class CustomLoginView(APIView):
    """Session-based login view. Accepts username and password,
    authenticates the user, and starts a session. """
    @extend_schema(
        tags=['Users'],
        request=LoginSerializer,
        responses={
            200: LoginSuccessResponseSerializer,
            400: LoginSerializer
        },
        summary="Session-based login",
        description="Authenticates user using username and password and starts a session."
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Create a session
            return Response({'message': 'Login successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

