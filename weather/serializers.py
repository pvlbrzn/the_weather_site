from rest_framework import serializers
from .models import WeatherQuery


# Сериализатор преобразует объекты Django в JSON (и наоборот)
class WeatherQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherQuery
        fields = '__all__'