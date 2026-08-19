from django.urls import path
from accounts.views import register, login_view, logout_view, edit_user, delete_user

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_user, name='edit_user'),
    path('delete_profile/', delete_user, name='delete_user'),
]