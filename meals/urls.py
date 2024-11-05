from django.contrib import admin
from django.urls import include, path
from meals import views

urlpatterns = [
    path('meals/', views.get_all_meals, name="get_all_foods"),
    path('users/', views.get_all_users,name='get_all_users'),
    path('register/', views.register, name="register"),
    path('add_meals/', views.add_meals, name="add_meals"),
    path('meals_list_search/', views.meals_list_search, name='meals_list_search'),
    path('user_search/', views.user_search, name='user_search'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
]
