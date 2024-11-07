from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from foods.models import Food, Food_type
from meals.models import Meal, User
from meals.serializers import MealSerializer, UserSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
def get_all_meals(request):
    print("USER IS:",request.user)
    meals = Meal.objects
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_meals(request):
    #if request.method == 'POST':
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        newMeal = serializer.save()
        return Response(f'user is {newMeal.user} and time is {newMeal.time}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def meals_list_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            # Filter meals based on a keyword in Food_type's name field
            # meals = Meal.objects.filter(
            #     # food_info__types__type__name__icontains=keyword  # Check if any Food linked to Meal has the name containing keyword
            #     food_info__types__type__icontains=keyword)
            meals = Meal.objects.filter(
    Q(food_info__types__type__icontains=keyword) | Q(food_info__name__icontains=keyword))
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
        hashed_password = make_password(password)
        newUser = User(name=name, email=email,age=age, goal=goal,password=hashed_password)       
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

# @permission_classes([IsAdminUser]) instead of api_view
@api_view(['GET'])
def get_all_users(request):
    users = User.objects
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            # Filter meals based on a keyword in user's name field
            users = User.objects.filter(name__icontains=keyword).distinct()
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # adds user requires post
    # elif request.method == 'POST':
    #      serializer = MealSerializer(data=request.data)
    #      if serializer.is_valid():
    #          serializer.save()
    #          return Response(serializer.data, status=status.HTTP_201_CREATED)
    #      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # user.delete()
    user.is_active = False
    user.save()
    # serializer = UserSerializer(user)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(f'user is  id {user.name} id: {user.id} active={user.isActive}', status=status.HTTP_200_OK)

@api_view(['PATCH'])
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    meal.delete()
    return Response(f'meal id {meal_id} is deleted')

#gpt example:
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from .models import User
# from .serializers import UserSerializer


#  @api_view(['PATCH'])
# def update_user_goal(request, user_id):
#     """
#     Update the 'goal' field of a user given their user ID.
#     """
#     # Fetch the user object or return a 404 if not found
#     user = get_object_or_404(User, id=user_id)
    
#     # Check if 'goal' is in the request data
#     if 'goal' not in request.data:
#         return Response({"error": "Please provide the 'goal' field to update."}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Update the 'goal' field
#     user.goal = request.data['goal']
#     user.save()
    
#     # Optional: Return the updated user data
#     serializer = UserSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# for the frontend:
@api_view(['GET'])
def meals_by_date(request):
    selected_date = request.GET.get('date')

    # Validate date format
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    # Filter meals by date
    meals = Meal.objects.filter(date=selected_date)

    # Prepare JSON response
    meals_data = [
        {
            "time": meal.time.strftime("%H:%M"),
            "foods": [food.name for food in meal.food_info.all()]
        }
        for meal in meals
    ]
    return JsonResponse({"meals": meals_data})

def daily_meals_view(request):
    return render(request, 'daily_meals.html')