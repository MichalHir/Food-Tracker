from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from meals.models import Meal
from meals.serializers import MealSerializer
from rest_framework import status
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import authenticate
from foods.models import Food, Food_type
from django.contrib.auth import get_user_model
from users.models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser



# Create your views here.
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_all_meals(request):
    print("USER IS:", request.user)
    meals = Meal.objects
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def meals_list_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == "GET":
        keyword = request.GET.get("keyword")
        if keyword:
            meals = Meal.objects.filter(
                Q(food_info__types__type=keyword)
                | Q(food_info__name__icontains=keyword)
            )
        else:
            meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for the frontend meals display:
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure this view requires authentication
def meals_by_date(request):
    date = request.GET.get("date")
    username = request.user.id  # Access the authenticated user's ID
    if date:
        meals = Meal.objects.filter(date=date).prefetch_related(
            "food_info"
        )
    
        formatted_meals = []
        for meal in meals:
            username =meal.user.username
            userID=meal.user.id
            foods = [
                food.name for food in meal.food_info.all()
            ]  # Get the list of food names for each meal
            if (userID==request.user.id):
                formatted_meals.append(
                    {
                        "meal_id":meal.id,
                        "time": meal.time.strftime("%H:%M"),  # Format time as needed
                        "foods": foods,
                        "username": username,
                        "userID":userID
                    }
            )

        # Prepare the response data
        response_data = {"meals": formatted_meals}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Date parameter is required"}, status=400)

class daily_meals_view(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request):
        print("request:",request)
        date = request.GET.get('date')
        if date:
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()
            meals = Meal.objects.filter(date=selected_date)
            serializer = MealSerializer(meals, many=True)
            return Response({"meals": serializer.data})
        return Response({"meals": []})
    

@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_meal( request,meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
        meal.delete()
        return Response({"message": "Meal deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Meal.DoesNotExist:
        return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)

    # for login


@api_view(["POST"])
@permission_classes([AllowAny])  # Ensure this view is accessible without authentication
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # Validate email and password presence
    if not email or not password:
        return Response(
            {"success": False, "message": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )


    try:
        # Attempt to retrieve the user by email
        user = MyUser.objects.get(email=email)
        username = user.username  # Get the username associated with this email
    except MyUser.DoesNotExist:
        return Response(
            {"success": False, "message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Authenticate using the username (since authenticate requires username, not email)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Generate JWT tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    else:
        # Failed authentication
        return Response(
            {"success": False, "message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # for add meal
MyUser = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])  # Ensure this view is accessible without authentication
def food_list(request):
    print("Accessing food_list view")  # Debugging statement to confirm access
    foods = Food.objects.all()
    food_data = []
    for food in foods:
        food_types = food.types.values_list(
            "type", flat=True
        )  # Get names of related Food_types
        food_data.append(
            {
                "id": food.id,
                "name": food.name,
                "types": list(food_types),  # Include types for each food
            }
        )
    # return JsonResponse(food_data, safe=False)
    return Response(food_data)

@api_view(['GET'])
@permission_classes([AllowAny])  # Ensure this view is accessible without authentication
def food_type_list(request):
    food_types = Food_type.objects.all().values("id", "type")
    return Response(list(food_types))


# MyUser = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])  # Ensure this view is accessible without authentication
def add_meal(request):
    if request.method == "POST":
        user_id = request.data.get("user")
        date = request.data.get("date")
        time = request.data.get("time")
        food_info = [int(item) for item in request.data.get("food_info", [])]  # Explicitly convert each item to an integer
    if not user_id or not date or not time or not food_info:
        return Response(
            {"status": "error", "message": "All fields are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = MyUser.objects.get(id=user_id)
        meals = Meal.objects.create(user=user, date=date, time=time)
        # Retrieve and link food items to the meal
        foods = Food.objects.filter(id__in=food_info)
        if not foods.exists():
                return Response(
                    {"status": "error", "message": "No valid food items found."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        meals.food_info.set(foods)  # Link the selected foods to the meal
        meals.save()
        print("added in backend")
        # Return success response
        return Response(
            {"status": "success"},
            status=status.HTTP_201_CREATED,
        )

    except MyUser.DoesNotExist:
            return Response(
                {"status": "error", "message": "User not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
@permission_classes([AllowAny])  # Ensure this view is accessible without authentication
def user_list(request):
    users = MyUser.objects.all().values("id", "username")
    return Response(list(users))

# for render home page
def home_view(request):
    return render(request, 'daily_meals.html')
