from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Seminar, Category
from .forms import NewSeminarForm
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def new_seminar(request):
    if request.method == 'POST':
        form = NewSeminarForm(request.POST, request.FILES)
        if form.is_valid():
            seminar = form.save(commit=False)
            seminar.teacher = request.user
            form.save()
            return redirect('core:seminar_list')
    else:
        form = NewSeminarForm()
    return render(request, 'core/new_seminar.html', context={'form':form})

def seminar_detail(request, seminar_id):
    seminar = Seminar.objects.get(id=seminar_id)
    is_joined = seminar.participants.filter(id=request.user.id).exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        seminar.participants.add(request.user)
        return redirect('core:seminar_detail', seminar_id=seminar_id)
    return render(request, 'core/seminar_detail.html', context={'seminar':seminar, 'is_joined':is_joined})

def seminar_list(request):
    query_params = request.GET.copy()
    query_params.pop("page", None)
    category_id = request.GET.get("category")
    search = request.GET.get("search")
    seminars = Seminar.objects.all()
    current_category = None

    SORT_OPTION = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'price_high': '-price',
        'price_low': 'price',
    }

    if category_id:
        seminars = seminars.filter(category_id=category_id)
        current_category = Category.objects.get(id=category_id)
    if search:
        seminars = seminars.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    sort = request.GET.get('sort', 'newest')
    seminars = seminars.filter(is_deleted=False).order_by(SORT_OPTION.get(sort, '-created_at'))

    paginator = Paginator(seminars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/seminar_list.html', context={'page_obj':page_obj, 'current_category': current_category, 'query_params': query_params.urlencode(), 'sort': sort})

def home(request):
    seminars = Seminar.objects.filter(is_deleted=False).order_by('-created_at')[:4]
    return render(request, 'core/home.html', context={'seminars':seminars})

@login_required
def edit_seminar(request, seminar_id):
    seminar = Seminar.objects.get(pk=seminar_id)
    if request.method == 'POST':
        form = NewSeminarForm(request.POST, request.FILES, instance=seminar)
        if form.is_valid():
            form.save()
        return redirect('core:seminar_detail', seminar_id=seminar.id)
    else:
        form = NewSeminarForm(instance=seminar)
    return render(request, 'core/edit_seminar.html', context={'form':form, 'seminar':seminar})

@login_required
def delete_seminar(request, seminar_id):
    Seminar.objects.filter(id=seminar_id).update(is_deleted=True)
    return redirect('core:seminar_list')
