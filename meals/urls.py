from django.contrib import admin
from django.urls import include, path
from meals import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("meals/", views.get_all_meals, name="get_all_foods"),
    path("add_meal/", views.add_meal, name="add_meals"),
    path("meals_list_search/", views.meals_list_search, name="meals_list_search"),
    # for daily meals
    path("daily-meals/", views.daily_meals_view.as_view(), name="daily_meals_view"),  
    path("meals_by_date/", views.meals_by_date, name="meals_by_date"),  # API URL for meals by date
    path('delete_meals/<int:meal_id>/', views.delete_meal, name='meal-detail'), # API URL for delete meal
    # for login
    path("api/login/", views.login_view, name="login"),  
    # for add meal
    path("api/foods/", views.food_list, name="food_list"),
    path("api/food_types/", views.food_type_list, name="food_type_list"),  # Optional
    path("add_meals/", views.add_meal, name="add_meal"),
    path("api/users/", views.user_list, name="user_list"),
    path("api/add_meals/", views.add_meal, name="add_meal")
]
