from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from foods.models import Food
from foods.serializers import FoodSerializer

# Create your views here.
@api_view(['GET'])

def get_all_foods(request):
    print("USER IS:",request.user)
    foods = Food.objects
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


# def get_admin_tasks(request):
#     print("USER IS:",request.user)
#     tasks = Task.objects.all()
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)

