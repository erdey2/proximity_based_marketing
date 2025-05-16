from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path("", UserListView.as_view(), name='user_list'),
    # path("register/", UserListView.as_view(), name="register"),
    # path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("session-login/", CustomLoginView.as_view(), name="custom_login"),
    # path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]