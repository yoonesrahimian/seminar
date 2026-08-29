from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from blog.forms import NewPostForm

@login_required
def new_post(request):
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

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', context={'page_obj': page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    recent_posts = Post.objects.order_by('-created_at').exclude(id=post.id)[:3]

    return render(request, 'blog/post_detail.html', context={'post': post, 'recent_posts': recent_posts})