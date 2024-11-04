from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from foods.models import Food, Food_type
from meals.models import Meal, User
from meals.serializers import MealSerializer, UserSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def get_all_meals(request):
    print("USER IS:",request.user)
    meals = Meal.objects
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def meals_list_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            # Filter meals based on a keyword in Food_type's name field
            meals = Meal.objects.filter(
                food_info__name__icontains=keyword  # Check if any Food linked to Meal has the name containing keyword
            ).distinct()
        else:
            meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
         serializer = MealSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        name=request.data['name']
        email=request.data['email']
        password=request.data['password']
        age=request.data['age']
        goal=request.data['goal']
        newUser = User(name=name, email=email,age=age, goal=goal,password=password)       
        newUser.is_active = True
        # newUser.set_password(password)  # Securely hash the password
        newUser.save()
        return Response(f'username is {newUser.name}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# or:
# @api_view(['POST'])
# def add_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({"message": f"User {user.username} created successfully"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def add_meals(request):
    #if request.method == 'POST':
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        newMeal = serializer.save()
        return Response(f'user is {newMeal.user} and time is {newMeal.time}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      