from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

User = get_user_model()

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs.get("username"),
            password=attrs.get("password")
        )

        if not user:
            raise ValidationError("Invalid credentials.")

        if not user.is_active:
            raise ValidationError("User is inactive.")

        # Set user on serializer
        self.user = user

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Return tokens and user info
        return {
            "refresh": str(refresh),
            "access": str(access),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                # Add more fields if needed
            }
        }



