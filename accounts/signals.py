from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from employee.models import Employee

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    print("Signal Triggered")
    print("instance", instance)
    if created:
        Employee.objects.create()