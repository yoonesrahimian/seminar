from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Content', config_name='default')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def image_url(self):
        if self.featured_image:
            return self.featured_image.url
        return '/static/images/default_post_image.png'

    def __str__(self):
        return self.title