from rest_framework import serializers
from foods.models import Food
from foods.serializers import FoodSerializer
from meals.models import Meal, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'goal', 'isActive']  # You can also specify fields explicitly if needed

class MealSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    food_info = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), many=True)  # Accepts list of Food IDs
    class Meta:
        model = Meal
        fields = ['id', 'user', 'date', 'time', 'food_info']  # You can also specify fields explicitly if needed