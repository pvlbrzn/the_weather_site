import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherQuery
from .serializers import WeatherQuerySerializer
from django.shortcuts import render

API_KEY = '505299ce6b11c58eda648de4ff5a0aac'


class WeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'City parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'error': 'City not found or API error'}, status=response.status_code)

        data = response.json()
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        }

        query = WeatherQuery.objects.create(**weather_data)
        serializer = WeatherQuerySerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


def weather_page(request):
    city = request.GET.get('city', None)
    weather_data = None
    error_message = None

    # Инициализируем просмотренные города как список словарей
    viewed_cities = request.session.get('viewed_cities', [])

    # Если данные в сессии не соответствуют ожидаемому формату, сбрасываем их
    if not isinstance(viewed_cities, list) or any(not isinstance(c, dict) for c in viewed_cities):
        viewed_cities = []
        request.session['viewed_cities'] = viewed_cities

    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            error_message = f"Ошибка при запросе данных о погоде: {e}"
        else:
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                }

                # Проверяем, есть ли город в просмотренных
                if not any(c['city'] == weather_data['city'] for c in viewed_cities):
                    viewed_cities.append(weather_data)
                    request.session['viewed_cities'] = viewed_cities
            else:
                error_message = "Город не найден или произошла ошибка API."

    return render(request, 'weather_page.html', {
        'weather_data': weather_data,
        'error_message': error_message,
        'viewed_cities': viewed_cities,
    })
