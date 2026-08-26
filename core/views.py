from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Seminar, Category, Review
from core.forms import NewSeminarForm, ReviewForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import User
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlencode
from django.utils.timezone import localtime

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
    seminar = get_object_or_404(Seminar, id=seminar_id)
    is_joined = seminar.participants.filter(id=request.user.id).exists()
    related_seminars = Seminar.objects.filter(category=seminar.category).exclude(id=seminar.id).order_by('-created_at')[:4]
    session_start = localtime(seminar.session_start)
    session_end = localtime(seminar.session_end)
    calendar_params = {
        'action': 'TEMPLATE',
        'text': seminar.title,
        'details': seminar.description,
        'location': seminar.location,
        'dates': (session_start.strftime('%Y%m%dT%H%M%S') + '/' + session_end.strftime('%Y%m%dT%H%M%S')),
        'ctz': 'Asia/Tehran'
    }
    google_calendar_url = ('https://calendar.google.com/calendar/render?' + urlencode(calendar_params))
    review_form = ReviewForm()
    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(seminar=seminar, user=request.user).exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        seminar.participants.add(request.user)
        return redirect('core:seminar_detail', seminar_id=seminar_id)
    return render(request, 'core/seminar_detail.html', context={'seminar':seminar, 'is_joined':is_joined, 'review_form':review_form, 'has_reviewed':has_reviewed, 'google_calendar_url': google_calendar_url, 'related_seminars': related_seminars})

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

@login_required
def create_review(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    is_joined = seminar.participants.filter(id=request.user.id).exists()

    if request.user not in seminar.participants.all():
        messages.error(request, 'You must join this seminar before reviewing it.')
    if Review.objects.filter(seminar=seminar, user=request.user).exists():
        messages.error(request, 'You have already reviewed this seminar.')

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.seminar = seminar
            review.user = request.user
            review.save()

            messages.success(request, 'Your review was added successfully.')
            return redirect('core:seminar_detail', seminar_id=seminar_id)
        return render(request, 'core/seminar_detail.html', context={'seminar':seminar, 'is_joined':is_joined, 'review_form':form, 'review_form_open':True})
    return redirect('core:seminar_detail', seminar_id=seminar_id)

@login_required
@require_POST
def toggle_favorite(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)

    if request.user.favorite_seminars.filter(id=seminar_id).exists():
        request.user.favorite_seminars.remove(seminar)
    else:
        request.user.favorite_seminars.add(seminar)

    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('seminar_detail', seminar_id=seminar_id)