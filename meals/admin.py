from django.contrib import admin
from foods.models import Food
from meals.models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Food)