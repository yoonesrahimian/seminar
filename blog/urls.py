from django.urls import path
from blog.views import post_list, post_detail, new_post, blog_home, edit_post, delete_post

app_name = 'blog'

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('list/', post_list, name='post_list'),
    path('new/', new_post, name='new_post'),
    path('edit/<slug:slug>/', edit_post, name='edit_post'),
    path('delete/<slug:slug>/', delete_post, name='delete_post'),
    path('<slug:slug>/', post_detail, name='post_detail'),
]