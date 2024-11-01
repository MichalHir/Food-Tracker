from django.contrib import admin
from foods.models import Food, Food_type

# Register your models here.
admin.site.register(Food)
admin.site.register(Food_type)