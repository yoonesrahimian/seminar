from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Seminar, Category
from .forms import NewSeminarForm
from datetime import datetime, date
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html')

# @login_required()
# def new_seminar(request):
#     errors = {}
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         discription = request.POST.get('discription')
#         location = request.POST.get('location')
#         price = request.POST.get('price')
#         session_date = request.POST.get('session_date')
#         session_time_start = request.POST.get('session_time_start')
#         session_time_end = request.POST.get('session_time_end')
#         is_public = request.POST.get('is_public') == 'true'
#         is_inperson = request.POST.get('is_inperson') == 'true'
#         image = request.FILES.get('image')
#         teacher = request.user
#         Seminar.objects.create(
#             title=title,
#             discription=discription,
#             location=location,
#             price=price,
#             is_public=is_public,
#             is_inperson=is_inperson,
#             image=image,
#             teacher=teacher,
#             session_date=session_date,
#             session_time_start=session_time_start,
#             session_time_end=session_time_end,
#         )
#         return redirect('seminar_list')
#     return render(request, 'core/new_seminar.html')

@login_required()
def new_seminar(request):
    if request.method == 'POST':
        form = NewSeminarForm(request.POST, request.FILES)
        if form.is_valid():
            seminar = form.save(commit=False)
            seminar.teacher = request.user
            form.save()
            return redirect('seminar_list')
    else:
        form = NewSeminarForm()
    return render(request, 'core/new_seminar.html', context={'form':form})

def seminar_detail(request, seminar_id):
    seminar = Seminar.objects.get(id=seminar_id)
    is_joined = seminar.participants.filter(id=request.user.id).exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        seminar.participants.add(request.user)
        return redirect('seminar_detail', seminar_id=seminar_id)
    return render(request, 'core/seminar_detail.html', context={'seminar':seminar, 'is_joined':is_joined})

def seminar_list(request):
    query_params = request.GET.copy()
    query_params.pop("page", None)
    category_id = request.GET.get("category")
    search = request.GET.get("search")
    seminars = Seminar.objects.all()
    current_category = None
    if category_id:
        seminars = seminars.filter(category_id=category_id)
        current_category = Category.objects.get(id=category_id)
    if search:
        seminars = seminars.filter(Q(title__icontains=search) | Q(description__icontains=search))
    paginator = Paginator(seminars, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/seminar_list.html', context={"page_obj":page_obj, "current_category": current_category, "query_params": query_params.urlencode()})

def home(request):
    seminars = Seminar.objects.order_by('-created_at')[:4]
    return render(request, 'core/home.html', context={'seminars':seminars})

def edit_seminar(request, seminar_id):
    # seminar = Seminar.objects.filter(id=seminar_id).first()
    seminar = Seminar.objects.get(pk=seminar_id)
    if request.method == 'POST':
        form = NewSeminarForm(request.POST, request.FILES, instance=seminar)
        if form.is_valid():
            form.save()
        # seminar.title = request.POST.get('title')
        # seminar.discription = request.POST.get('discription')
        # seminar.location = request.POST.get('location')
        # seminar.price = request.POST.get('price')
        # seminar.session_date = request.POST.get('session_date')
        # seminar.session_time_start = request.POST.get('session_time_start')
        # seminar.session_time_end = request.POST.get('session_time_end')
        # seminar.is_public = request.POST.get('is_public') == 'true'
        # seminar.is_inperson = request.POST.get('is_inperson') == 'true'
        # seminar.image = request.FILES.get('image')
        # seminar.teacher = request.user
        # seminar.participant = '{}'
        # seminar.save()
        return redirect('seminar_detail', seminar_id=seminar.id)
    else:
        form = NewSeminarForm(instance=seminar)
    return render(request, 'core/edit_seminar.html', context={'form':form, 'seminar':seminar})

def delete_seminar(request, seminar_id):
    Seminar.objects.filter(id=seminar_id).delete()
    return redirect('seminar_list')
