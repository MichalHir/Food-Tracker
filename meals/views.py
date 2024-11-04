from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from foods.models import Food_type
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
def meals_list_sort(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        type_id = request.GET.get('type_id')
        if type_id:
            # Get the category object
            # type = Food_type.objects.get(id=type_id)
            # Retrieve the category object or return 404 if it doesn't exist
            food_type = get_object_or_404(Food_type, id=type_id)                
            # Filter products that belong to the selected category
            meals = Meal.objects.filter(food_type=food_type)
        else:
            meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
    #     print("json recieved is:", request.data)
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
# ask:
# @api_view(['POST'])
# def add_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({"message": f"User {user.username} created successfully"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# input:  {
#    "username": "monika",
#    "email": "monika@gmail.com",
#    "password": "password123",
#    "age": 18,
#    "goal": "health"
# }


# input:  {
#   "user": 1,         # User ID for ForeignKey
#   "date": "2024-11-02",
#   "time": "12:30:00",
#   "food_info": [1, 2, 3]  # List of Food IDs for Many-to-Many
# }  

@api_view(['POST'])
def add_meals(request):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        # user=request.data['user']
        # date=request.data['date']
        # time=request.data['time']
        # food_info=request.data['food_info']
        # newMeal = Meal(user=user, date=date,time=time, food_info=food_info)       
        # newMeal.save()
        newMeal = serializer.save()
        return Response(f'user is {newMeal.user} and time is {newMeal.time}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      