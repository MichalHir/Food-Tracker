from django.contrib import admin
from django.urls import include, path
from meals import views

urlpatterns = [
    path('meals/', views.get_all_meals, name="get_all_foods"),
    path('register/', views.register, name="register"),
    path('add_meals/', views.add_meals, name="add_meals"),
    path('add_meals_sort/', views.meals_list_sort, name="meals_list_sort")
]
