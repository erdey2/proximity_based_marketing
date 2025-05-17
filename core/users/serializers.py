from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

user = get_user_model()

class CustomLoginSerializer(LoginSerializer):
    print("✅ CustomLoginSerializer being used!")
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken.for_user(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data

