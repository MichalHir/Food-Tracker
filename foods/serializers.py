from rest_framework import serializers
from .models import Food, Food_type

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_type
        fields = '__all__'  # or specify fields explicitly if needed

class FoodSerializer(serializers.ModelSerializer):
    types = FoodTypeSerializer(many=True, read_only=True)  # Nested serializer for types

    class Meta:
        model = Food
        fields = '__all__'  # or specify fields explicitly
