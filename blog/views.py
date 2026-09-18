from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from blog.forms import NewPostForm
from django.db.models import Q

@login_required
def new_post(request):
    if not request.user.is_staff:
        return redirect('blog:blog_home')
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = NewPostForm()
    return render(request, 'blog/new_post.html', context={'form': form})

# def post_list(request):
#     category_id = request.GET.get('category')
#     search = request.GET.get("search")

#     posts = Post.objects.filter(is_published=True).order_by('-created_at')
#     if category_id:
#         posts = posts.filter(category_id=category_id)
#         current_category = Category.objects.get(id=category_id)
#     if search:
#         seminars = seminars.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
#     paginator = Paginator(posts, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'blog/post_list.html', context={'page_obj': page_obj})

def post_list(request):
    query_params = request.GET.copy()
    query_params.pop("page", None)
    category_id = request.GET.get("category")
    search = request.GET.get("search")
    posts = Post.objects.filter(is_published=True, is_deleted=False)
    current_category = None

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        posts = posts.filter(category_id__in=current_category.get_descendant_ids())
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(short_description__icontains=search))

    posts = posts.order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', context={'page_obj':page_obj, 'current_category': current_category, 'query_params': query_params.urlencode()})

def blog_home(request):
    posts = Post.objects.filter(is_published=True, is_deleted=False).order_by('-published_at')[:3]
    first_post = posts[0] if posts else None
    posts = posts[1:3]
    return render(request, 'blog/blog_home.html', context={'first_post': first_post, 'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.order_by('-published_at').exclude(id=post.id)[:3]
    recent_user_posts = Post.objects.filter(author=post.author, is_published=True, is_deleted=False).order_by('-published_at').exclude(id=post.id)[:3]
    if not post.is_published:
        if request.user == post.author:
            return render(request, 'blog/post_detail.html', context={'post': post, 'recent_posts': recent_posts, 'recent_user_posts': recent_user_posts})
        else:
            return redirect('blog:blog_home')
    return render(request, 'blog/post_detail.html', context={'post': post, 'recent_posts': recent_posts, 'recent_user_posts': recent_user_posts})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = NewPostForm(instance=post)
    return render(request, 'blog/edit_post.html', context={'form': form, 'post': post})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, is_deleted=False)
    post.is_deleted = True
    post.save(update_fields=['is_deleted'])
    return redirect('dashboard:my_blogs')

def category_post(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category_id__in=category.get_descendant_ids(), is_published=True, is_deleted=False)

    # query = request.GET.get('q', '').strip()
    # if query:
    #     posts = posts.filter(Q(title__incontains=query) | Q(content__icontains=query))

    posts.order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', context={'page_obj': page_obj, 'current_category': category, 'query_params': None, 'is_category_page': True})