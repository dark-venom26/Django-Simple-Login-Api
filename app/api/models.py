from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.username