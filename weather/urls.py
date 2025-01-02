'''
Weather URL Configuration
'''
from django.urls import path
from .views import WeatherDetail

urlpatterns = [
    path('<str:country_code>/<str:zip_code>', WeatherDetail.as_view(), name='weather-detail'),
]
