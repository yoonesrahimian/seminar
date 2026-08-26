from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, Notification
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, EditUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:profile')
    else:
        form = EditUserForm(instance=user)
    return render(request, "accounts/edit_user.html", context={'form': form, 'user': user})

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', context={'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return redirect('dashboard:notifications')