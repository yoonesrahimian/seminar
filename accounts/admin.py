from django.contrib import admin
from accounts.models import User, Notification

admin.site.register(User)
admin.site.register(Notification)