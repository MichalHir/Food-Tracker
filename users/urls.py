

from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('users/', views.get_all_users,name='get_all_users'),
    path('user_search/', views.user_search, name='user_search'),
]