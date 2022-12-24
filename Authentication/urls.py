from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('token/', TokenRefreshView.as_view()),
    path('login/', LoginView.as_view()),
    path('twofactor/', VerifyTwoFactorOTPView.as_view()),
]