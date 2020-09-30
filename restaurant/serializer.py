from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name_restaurant','stars','delivery','genre')
        model = Restaurant