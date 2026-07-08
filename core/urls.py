from django.urls import path
from core.views import new_seminar, seminar_detail, seminar_list, edit_seminar, delete_seminar

urlpatterns = [
    path('new_seminar/', new_seminar, name='new_seminar'),
    path('seminar_detail/<seminar_id>/', seminar_detail, name='seminar_detail'),
    path('seminar_list/', seminar_list, name='seminar_list'),
    path('edit_seminar/<seminar_id>/', edit_seminar, name='edit_seminar'),
    path('delete_seminar/<seminar_id>/', delete_seminar, name='delete_seminar'),
]