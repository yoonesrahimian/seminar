"""
URL configuration for seminar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from core.views import new_organization, edit_organization, delete_organization, send_organization_invitation, answer_organization_invitation, delete_organization_member

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('seminar/', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('blog/', include('blog.urls')),
    path('organization/new/', new_organization, name='new_organization'),
    path('organization/edit/<int:id>/', edit_organization, name='edit_organization'),
    path('organization/delete/<int:id>/', delete_organization, name='delete_organization'),
    path('organization/send-invitation/', send_organization_invitation, name='send_organization_invitation'),
    path('invitation/answer/', answer_organization_invitation, name='answer_invitation'),
    path('organization/member/delete/', delete_organization_member, name='delete_organization_member'),
    path('ckeditor5/', include('django_ckeditor_5.urls'))
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)