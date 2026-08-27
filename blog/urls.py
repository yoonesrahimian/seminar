from django.urls import path
from blog.views import post_list, post_detail, new_post

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('new/', new_post, name='new_post'),
    path('<slug:slug>/', post_detail, name='post_detail'),
]