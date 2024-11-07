from django.db import models
# Create your models here.
class Food_type(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Food(models.Model):
    name = models.CharField(max_length=255)  
    # type = models.CharField(max_length=255)
    types = models.ManyToManyField(Food_type, related_name='foods')  # Many-to-many relationship with Food_type
    # isHealthy = models.BooleanField(default=False)  # Done status (True/False

    def __str__(self):
        return self.name
    

