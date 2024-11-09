from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from meals.models import Meal
from meals.serializers import MealSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from foods.models import Food,Food_type
from django.contrib.auth import get_user_model
import json
from users.models import MyUser
from rest_framework.permissions import IsAuthenticated

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


# @api_view(['POST']) - move to admin
# def register(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         name=request.data['name']
#         email=request.data['email']
#         password=request.data['password']
#         age=request.data['age']
#         goal=request.data['goal']
#         hashed_password = make_password(password)
#         newUser = User(name=name, email=email,age=age, goal=goal,password=hashed_password)       
#         newUser.is_active = True
#         # newUser.set_password(password)  # Securely hash the password
#         newUser.save()
#         return Response(f'username is {newUser.name}')
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# or:
# @api_view(['POST'])
# def add_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({"message": f"User {user.username} created successfully"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @permission_classes([IsAdminUser]) instead of api_view
# @api_view(['GET']) - move to admin
# def get_all_users(request):
#     users = User.objects
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['GET']) - move to admin
# def user_search(request):
#     """
#     List all  products, or create a new product.
#     """
#     if request.method == 'GET':
#         keyword = request.GET.get('keyword')
#         if keyword:
#             # Filter meals based on a keyword in user's name field
#             users = User.objects.filter(name__icontains=keyword).distinct()
#         else:
#             users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        # adds user requires post
    # elif request.method == 'POST':
    #      serializer = MealSerializer(data=request.data)
    #      if serializer.is_valid():
    #          serializer.save()
    #          return Response(serializer.data, status=status.HTTP_201_CREATED)
    #      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def deactivate_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    # user.delete()
    user.is_active = False
    user.save()
    # serializer = UserSerializer(user)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(f'user is  id {user.name} id: {user.id} active={user.isActive}', status=status.HTTP_200_OK)

@api_view(['PATCH']) #go back to it
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

# for the frontend meals display:
def meals_by_date(request):
    date = request.GET.get('date')
    if date:
        # Retrieve meals filtered by the specified date
        # meals = Meal.objects.filter(date=date).prefetch_related('food_info')
        meals = Meal.objects.filter(date=date).prefetch_related('food_info')    # Format the meals data to include associated foods
        formatted_meals = []
        for meal in meals:
            foods = [food.name for food in meal.food_info.all()]  # Get the list of food names for each meal                
            formatted_meals.append({
            'time': meal.time.strftime('%H:%M'),  # Format time as needed
            'foods': foods
        })

         # Prepare the response data
        response_data = {'meals': formatted_meals}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)
   
    
class daily_meals_view(generics.ListAPIView):
    queryset = Meal.objects.all().select_related('user').prefetch_related('food_info__types')
    serializer_class = MealSerializer

    # for login
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Attempt to retrieve the user by email
        user = MyUser.objects.get(email=email)
        username = user.username  # Get the username associated with this email
    except MyUser.DoesNotExist:
        return Response({"success": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Authenticate using the username (since authenticate requires username, not email)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Successful authentication
        return Response({"success": True, "message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        # Failed authentication
        return Response({"success": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # for add meal
def food_list(request):
    foods = Food.objects.all()
    food_data = []
    for food in foods:
        food_types = food.types.values_list('type', flat=True)  # Get names of related Food_types
        food_data.append({
            'id': food.id,
            'name': food.name,
            'types': list(food_types),  # Include types for each food
        })
    return JsonResponse(food_data, safe=False)
def food_type_list(request):
    food_types = Food_type.objects.all().values('id', 'type')
    return JsonResponse(list(food_types), safe=False)

MyUser = get_user_model()

@csrf_exempt
def add_meal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user')
        date = data.get('date')
        time = data.get('time')
        food_ids = data.get('food_info', [])

        try:
            user = MyUser.objects.get(id=user_id)
            meal = Meal.objects.create(user=user, date=date, time=time)
            foods = Food.objects.filter(id__in=food_ids)
            meal.food_info.set(foods)  # Link the selected foods to the meal
            meal.save()
            return JsonResponse({'status': 'success', 'message': 'Meal added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
def user_list(request):
    users = MyUser.objects.all().values('id', 'username')  # Ensure username is correct attribute
    return JsonResponse(list(users), safe=False)