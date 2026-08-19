from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, EditUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme

# def register(request):
#     errors = {}
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         password = make_password(request.POST.get('password'))
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         country = request.POST.get('country')
#         city = request.POST.get('city')
#         profile_picture = request.FILES.get('profile_picture')
#         if User.objects.filter(username=username).exists():
#             errors['username'] = 'Username already exists.'
#         elif email and User.objects.filter(email=email).exists():
#             errors['email'] = 'email already exists.'
#         elif phone and User.objects.filter(phone=phone).exists():
#             errors['phone'] = 'phone already exists.'
#         else:
#             User.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 password=password,
#                 phone=phone,
#                 email=email,
#                 address=address,
#                 country=country,
#                 city=city,
#                 profile_picture=profile_picture,
#             )
#             return redirect('login')

#     return render(request, 'accounts/register.html', context={'errors':errors})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard:profile")
    else:
        form = EditUserForm(instance=user)
    return render(request, "accounts/edit_user.html", context={"form": form, "user": user})

def delete_user(request):
    user = request.user
    user.delete()
    return redirect("home")

def login_view(request):
    errors = {}
    if request.method == 'POST':
        # form = LoginForm(request.POST)
        form = LoginForm(request, data=request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        # if user:
            # login(request, user)
            # return redirect('home')
        # errors['user_pass'] = 'Username or Password is incorrect.' 
        # return render)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')
    # form = LoginForm()
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', context={'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')