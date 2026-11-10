import http
from operator import ge
import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.vary import vary_on_headers

@method_decorator(vary_on_headers("Authorization"), name="get")
class WeatherApp(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        key = f'weather:{request.user.id}'
        if cache.get(key):
            weatherData = cache.get(key)
            return Response(
                weatherData,
                status=status.HTTP_200_OK
            )
        else:
            location = settings.TIME_ZONE.partition('/')[2].replace('_', ' ')
            geoRequest = requests.get(
                f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={settings.OPENWEATHER_API_KEY}",
                timeout=5
            )
            if geoRequest.status_code != 200:
                return Response(
                    {
                        'detail': "Request Failed"
                    },
                    status=geoRequest.status_code
                )
            geoRequestData = geoRequest.json()[0]
            if not geoRequestData:
                return Response(
                    {
                        'detail': "Empty Search Result"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            latitude = geoRequestData['lat']
            longtitude = geoRequestData['lon']
            weatherRequest = requests.get(
                url='https://api.open-meteo.com/v1/forecast/',
                params={
                    "latitude": latitude,
                	"longitude": longtitude,
	                "daily": [
						"temperature_2m_max",
						"temperature_2m_min",
					],
					"current": [
					    "temperature_2m",
						"apparent_temperature",
						"relative_humidity_2m",
						"wind_speed_10m",
						"wind_direction_10m",
					],
	                "timezone": "auto",
	                "forecast_days": 1,
                },
                timeout=5
            )

            if weatherRequest.status_code != 200:
                return Response(
                    {
                        'detail': "Request Failed"
                    },
                    status=weatherRequest.status_code
                )

            weatherRequestData = weatherRequest.json()

            responseData = {
                'location': location,
                'current_temprature': str(weatherRequestData['current']['temperature_2m']) + " ℃",
                'apparent_temprature': str(weatherRequestData['current']['apparent_temperature']) + " ℃",
                'relative_humidity_2m': str(weatherRequestData['current']['relative_humidity_2m']),
                'max_temp_today': str(weatherRequestData['daily']['temperature_2m_max'][0]) + " ℃",
                'min_temp_today': str(weatherRequestData['daily']['temperature_2m_min'][0]) + " ℃",
                'wind_speed': str(weatherRequestData['current']['wind_speed_10m']) + " KM/H",
            }
            cache.set(key, responseData, timeout=1200)
            return Response(
                responseData,
                status=status.HTTP_200_OK
            )
