from django.db import models
from django.contrib.auth.models import AbstractUser

COUNTRY_CHOICES = [
    ("IR", "Iran"),
    ("TR", "Turkey"),
    ("AZ", "Azerbaijan"),
]

CITY_CHOICES = [
    ("TEH", "Tehran"),
    ("TBZ", "Tabriz"),
    ("MSH", "Mashhad"),
]

class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, unique=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=3, choices=CITY_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=True)
    # user_role = models.CharField(choices=('organizer','teacher','participant'), default='participant')
    # bio