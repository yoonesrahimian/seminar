from django.contrib import admin
from core.models import Seminar, Category, Review, Organization, OrganizationMembership

admin.site.register(Seminar)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(OrganizationMembership)
# admin.site.register(Session)
admin.site.register(Review)