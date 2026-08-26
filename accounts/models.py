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
    email = models.EmailField(unique=True, blank=True, null=True)
    # user_role = models.CharField(choices=('organizer','teacher','participant'), default='participant')
    # bio
    favorite_seminars = models.ManyToManyField(to='core.Seminar', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username

class Notification(models.Model):
    recipient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    related_seminar = models.ForeignKey(to='core.Seminar', on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.recipient.username} - {self.title}'