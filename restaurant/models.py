from django.db import models
from django.contrib.auth import get_user_model

class Restaurant(models.Model):
    name_restaurant = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    # waiters  = models.PositiveIntegerField()
    stars = models.PositiveIntegerField()
    delivery = models.BooleanField()
    genre = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name_restaurant)