from django.contrib import admin
from django.urls import include, path

from foods import views

urlpatterns = [
    path('foods/', views.get_all_foods, name="get_all_foods"),
    path('foods_list_search/', views.foods_list_search, name='foods_list_search'),
    # path('api/foods/', views.get_all_foods, name="get_all_foods"),
]