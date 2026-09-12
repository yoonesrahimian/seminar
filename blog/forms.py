from django import forms
from blog.models import Post, Category
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.text import slugify
from django.utils import timezone

class NewPostForm(forms.ModelForm):
    slug = forms.SlugField(required=False, help_text='Leave blank to automatically generate it from the title.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'featured_image', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = self.get_category_choices()
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()

    def get_category_choices(self):
        categories = Category.objects.select_related("parent").all()

        categories_by_parent = {}

        for category in categories:
            categories_by_parent.setdefault(
                category.parent_id,
                []
            ).append(category)

        choices = [
            ("", "--------- Select a category ---------")
        ]

        def add_categories(parent_id, level=0):
            children = categories_by_parent.get(parent_id, [])

            for category in children:
                choices.append(
                    (
                        category.pk,
                        f"{'— ' * level}{category.name}",
                    )
                )

                add_categories(category.pk, level + 1)

        add_categories(None)

        return choices
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title', ''))
        return slug

    def save(self, commit=True):
        post = super().save(commit=False)
        if post.is_published:
            post.published_at = timezone.now()
        else:
            post.published_at = None
        if commit:
            post.save()
        return post