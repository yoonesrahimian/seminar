from django import forms
from blog.models import Post
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.text import slugify

class NewPostForm(forms.ModelForm):
    slug = forms.SlugField(required=False, help_text='Leave blank to automatically generate it from the title.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'featured_image', 'category', 'is_published', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title', ''))
        return slug