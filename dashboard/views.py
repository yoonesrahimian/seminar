from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from core.models import Seminar

@login_required
def dashboard(request):
    my_seminars = Seminar.objects.filter(teacher=request.user).order_by("-created_at")[:3]
    joined_seminars = Seminar.objects.filter(participants=request.user).order_by("-created_at")[:3]
    return render(request, "dashboard/dashboard.html", context={"my_seminars":my_seminars, "joined_seminars":joined_seminars})

@login_required
def my_seminars(request):
    return render(request, "dashboard/my_seminars.html")

@login_required
def joined_seminars(request):
    return render(request, "dashboard/joined_seminar.html")

@login_required
def profile(request):
    user = request.user
    return render(request, "dashboard/profile.html", context={"user":user})