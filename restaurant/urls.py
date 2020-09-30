from django.urls import path
from .views import RestaurantList , RestaurantDetails

urlpatterns = [
    path('',RestaurantList.as_view(), name='rest_list'),
    path('<int:pk>',RestaurantDetails.as_view(), name='rest_details'),
]