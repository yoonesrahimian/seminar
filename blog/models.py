from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    
    def clean(self):
        if self.parent == self:
            raise ValidationError({"parent": "A category cannot be its own parent."})
        parent = self.parent

        while parent is not None:
            if parent == self:
                raise ValidationError({"parent": "A category cannot be its own descendant."})
            parent = parent.parent

    def get_ancestors(self):
        ancestors = []
        category = self.parent
        while category:
            ancestors.append(category)
            category = category.parent
        return ancestors[::-1]

    def get_descendant_ids(self):
        ids = [self.pk]
        for child in self.children.all():
            ids.extend(child.get_descendant_ids())
        return ids


    def get_breadcrumbs(self):
        return [*self.get_ancestors(), self]

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    content = CKEditor5Field('Content', config_name='default')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, blank=True, null=True, related_name='posts')
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