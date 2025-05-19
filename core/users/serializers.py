from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        # 1) Authenticate with username/password
        user = authenticate(
            request=self.context.get("request"),
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if not user:
            raise ValidationError("Invalid credentials.")

        if not user.is_active:
            raise ValidationError("User is inactive.")

        # 2) Assign the real User instance
        self.user = user

        # 3) Return a dict containing "user": user
        #    → This is exactly what the LoginView will look for.
        return {"user": user}

    def get_response_data(self, user):
        """
        After LoginView does jwt_encode(user), it will pass `user` here.
        super().get_response_data(user) already returns {"access": "...", "refresh": "..."}.
        We just append "user": { … } to that.
        """
        data = super().get_response_data(user)
        data["user"] = {
            "id":         user.id,
            "username":   user.username,
            "email":      user.email,
            "first_name": user.first_name,
            "last_name":  user.last_name,
        }
        return data





