from django.db import models
# from accounts.models import User
from django.contrib.auth.models import User
# Create your models here.

# Create a one to one relationship with the User model


class Employee(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE),
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    address=models.TextField(max_length=255, default='')
    department=models.CharField(max_length=255, default='')
    position=models.CharField(max_length=255, default='Employee')
    salary=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name