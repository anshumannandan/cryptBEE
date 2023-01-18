from django.urls import path
from .views import *


urlpatterns = [
    path('buy/', BuyCoinView.as_view()),
    path('sell/', SellCoinView.as_view()),
]
