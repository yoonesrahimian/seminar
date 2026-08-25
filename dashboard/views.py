from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Seminar

@login_required
def dashboard(request):
    my_seminars = Seminar.objects.filter(teacher=request.user, is_deleted=False).order_by('-created_at')[:3]
    joined_seminars = Seminar.objects.filter(participants=request.user, is_deleted=False).order_by('-created_at')[:3]
    return render(request, 'dashboard/dashboard.html', context={'my_seminars':my_seminars, 'joined_seminars':joined_seminars})

@login_required
def my_seminars(request):
    my_seminars = Seminar.objects.filter(teacher=request.user, is_deleted=False).order_by('-created_at')
    return render(request, 'dashboard/my_seminars.html', context={'my_seminars': my_seminars})

@login_required
def joined_seminars(request):
    joined_seminars = Seminar.objects.filter(participants=request.user, is_deleted=False).order_by('-created_at')
    return render(request, 'dashboard/joined_seminars.html', context={'joined_seminars': joined_seminars})

@login_required
def profile(request):
    user = request.user
    return render(request, 'dashboard/profile.html', context={'user':user})

@login_required
def favorite(request):
    favorite_seminars = request.user.favorite_seminars.all()
    return render(request, 'dashboard/favorite.html', context={'favorite_seminars': favorite_seminars})