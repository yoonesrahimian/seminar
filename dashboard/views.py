from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Seminar, Organization, OrganizationMembership
from blog.models import Post
from core.forms import OrganizationInvitationForm
from django.db.models import Q

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

@login_required
def notifications(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'dashboard/notifications.html', context={'notifications': notifications})

@login_required
def my_blogs(request):
    blogs = Post.objects.filter(author=request.user, is_deleted=False).order_by('-published_at')
    return render(request, 'dashboard/my_blogs.html', context={'blogs': blogs})

@login_required
def wallet(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.all().order_by('-created_at')
    return render(request, 'dashboard/wallet.html', context={'transactions': transactions, 'wallet': wallet})

@login_required
def organizations(request):
    organizations = Organization.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
    return render(request, 'dashboard/organizations.html', context={'organizations': organizations})

@login_required
def organization_detail(request, id):
    organization = get_object_or_404(Organization, id=id)
    members = OrganizationMembership.objects.filter(organization=organization)
    seminars = organization.seminars.all()

    context={
        'organization': organization,
        'invitation_form': OrganizationInvitationForm(initial={'organization_id': organization.id}),
        'members': members,
        'seminars': seminars,
        }
    return render(request, 'dashboard/organization_detail.html', context=context)