from django.urls import path
from weather.api.v1.views import WeatherApp

app_name = 'api-v1'

urlpatterns = [
    path('', WeatherApp.as_view(), name="weather-app"),
]
