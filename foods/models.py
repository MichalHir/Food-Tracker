from django.db import models

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=255)  # Task name
#     email = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     age = models.IntegerField(default=None)
#     goal= models.CharField(max_length=255, default=None)
    # isActive = models.BooleanField(default=False)  # Done status (True/False)
    
# class Task(models.Model):
#     name = models.CharField(max_length=255)  # Task name
#     deadline = models.DateField()             # Task deadline date
#     done = models.BooleanField(default=False)  # Done status (True/False)
#     user = models.ForeignKey(TaskUser, on_delete=models.CASCADE)  # Link to the User model



    # def __str__(self):
    #     return self.name
