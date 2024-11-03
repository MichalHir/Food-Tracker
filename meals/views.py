from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from meals.models import Meal, User
from meals.serializers import MealSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET'])

def get_all_meals(request):
    print("USER IS:",request.user)
    meals = Meal.objects
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    username=request.data['username'],
    email=request.data['email'],
    password=request.data['password'],
    age=request.data['age'],
    goal=request.data['goal'],
    newUser = User(username=username, email=email,age=age, goal=goal)       
    newUser.is_active = True
    newUser.set_password(password)  # Securely hash the password
    newUser.save()
    return Response(f'username is {newUser.name}')

@api_view(['POST'])
def add_meals(request):
    # class Meal(models.Model):
    # user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user',null=True)
    # date=models.DateField(auto_now_add=True)
    # time=models.TimeField(auto_now=True)
    # food_info = models.ManyToManyField(Food, related_name='meals')  # Many-to-Many relationship with Food
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        user=request.data['user'],
        date=request.data['date'],
        time=request.data['time'],
        food=request.data['food'],
        newMeal = Meal(user=user, date=date,time=time, food=food)       
        # newMeal.save()
        meal = serializer.save()
    return Response(f'user is {newMeal.user} and timt is {newMeal.time}')
      