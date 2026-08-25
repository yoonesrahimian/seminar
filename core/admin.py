from django.contrib import admin
from core.models import Seminar, Category, Review

admin.site.register(Seminar)
admin.site.register(Category)
# admin.site.register(Session)
admin.site.register(Review)