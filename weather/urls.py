from django.urls import path
from .views import WeatherView, weather_page

urlpatterns = [
    path('weather/', WeatherView.as_view(), name='weather'),
    path('', weather_page, name='weather-page')
]