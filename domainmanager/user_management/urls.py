from django.urls import path, include
from .views import Login, LogoutView, ForgotPassword, PasswordResetConfirmView

app_name = "user_management"

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot-password"),
    path("reset/<uidb64>/<token>/<email>/", PasswordResetConfirmView.as_view(), name="reset"),
]