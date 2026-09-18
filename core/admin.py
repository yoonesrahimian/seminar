from django.contrib import admin
from core.models import Seminar, Category, Review, Organization, OrganizationMember

admin.site.register(Seminar)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(OrganizationMember)
# admin.site.register(Session)
admin.site.register(Review)