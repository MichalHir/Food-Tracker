from django.db import models
from foods.models import Food
# from meals.serializers import MealSerializer

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
    
# for frontend
# class MealListView(generics.ListAPIView):
#     queryset = Meal.objects.all().select_related('user').prefetch_related('food_info__types')
#     serializer_class = MealSerializer