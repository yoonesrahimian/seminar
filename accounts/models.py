from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True)
    birthdate = models.DateField(null=True)
    country = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True)
    address = models.TextField(null=True)
    # user_role = models.CharField(choices=('organizer','teacher','participant'), default='participant')
    # bio