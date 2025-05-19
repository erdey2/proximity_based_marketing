from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer