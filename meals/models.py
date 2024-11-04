from django.db import models

from foods.models import Food

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)  
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    age = models.IntegerField(default=None)
    goal= models.CharField(max_length=255, default=None)
    isActive = models.BooleanField(default=True)  # Done status (True/False

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user',null=True)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now=True)
    food_info = models.ManyToManyField(Food, related_name='meals')  # Many-to-Many relationship with Food

    def __str__(self):
        return f"{self.time} - {self.food_info}"