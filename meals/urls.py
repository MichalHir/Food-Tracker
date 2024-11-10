from django.contrib import admin
from django.urls import include, path
from meals import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("meals/", views.get_all_meals, name="get_all_foods"),
    path("add_meal/", views.add_meals, name="add_meals"),
    path("meals_list_search/", views.meals_list_search, name="meals_list_search"),
    path("daily-meals/", views.daily_meals_view.as_view(), name="daily_meals_view"),  # Add .as_view()  # URL for the HTML page
    path("meals_by_date/", views.meals_by_date, name="meals_by_date"),  # API URL for meals by date
    # for login
    path("api/login/", views.login_view, name="login"),  # This sets up the /api/login/ route
    # path('api/login/', obtain_auth_token, name='api_token_auth'),
    # for add meal
    path("api/foods/", views.food_list, name="food_list"),
    path("api/food_types/", views.food_type_list, name="food_type_list"),  # Optional
    path("add_meals/", views.add_meal, name="add_meal"),
    path("api/users/", views.user_list, name="user_list"),
    path("api/add_meals/", views.add_meal, name="add_meal")
]
