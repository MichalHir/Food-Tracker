from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from users.models import MyUser
from users.serializers import MyUserSerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to anyone
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if MyUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = MyUser(username=username, email=email)
    user.password = make_password(password)  # Hash the password
    user.save()
    
    return Response({"message": f"User {user.username} created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # Only allow access to admin users
def get_all_users(request):
    users = MyUser.objects.all()  # Retrieve all users
    serializer = MyUserSerializer(users, many=True)  # Serialize the list of users
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            # Filter meals based on a keyword in user's name field
            users = MyUser.objects.filter(username__icontains=keyword).distinct()
        else:
            users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
         serializer = MyUserSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

