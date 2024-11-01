from rest_framework import serializers
from foods.serializers import FoodSerializer
from meals.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # You can also specify fields explicitly if needed

class MealSerializer(serializers.ModelSerializer):
    food_info = FoodSerializer(many=True, read_only=True)  # Nested serializer
    class Meta:
        model = User
        fields = '__all__'  # You can also specify fields explicitly if needed