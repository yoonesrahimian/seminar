from blog.models import Category


def blog_categories(request):
    return {'blog_categories': Category.objects.all()}