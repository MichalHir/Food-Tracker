from django.contrib import admin
from meals.models import Meal, User

# Register your models here.
admin.site.register(User)
admin.site.register(Meal)