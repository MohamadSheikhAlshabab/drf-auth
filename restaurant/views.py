from django.shortcuts import render
from rest_framework import generics
from .models import Restaurant
from .serializer import RestaurantSerializer
from .permissions import IsName_RestaurantOrReadOnly
from rest_framework import permissions

class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsName_RestaurantOrReadOnly,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer