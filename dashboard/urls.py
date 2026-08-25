from django.urls import path
from dashboard.views import dashboard, profile, my_seminars, joined_seminars, favorite

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('my_seminars/', my_seminars, name='my_seminars'),
    path('joined_seminars/', joined_seminars, name='joined_seminars'),
    path('favorite/', favorite, name='favorite')
]