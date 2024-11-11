from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from foods.models import Food, Food_type
from foods.serializers import FoodSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET'])

def get_all_foods(request):
    print("USER IS:",request.user)
    foods = Food.objects
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def foods_list_search(request):
    """
    List all  products, or create a new product.
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        type_id = None
        for food_type in Food_type.objects.all():
            if keyword.lower() in food_type.type.lower():  # Case-insensitive match
                type_id = food_type.id
                break  # Return None if no match is found
        if keyword:
            # Filter meals based on a keyword in Food_type's name field (e.g., 'carbs')
            foods = Food.objects.filter(types=type_id).distinct()
        else:
            foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
    #     print("json recieved is:", request.data)
         serializer = FoodSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

