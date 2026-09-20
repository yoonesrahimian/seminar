from django.db import models
from django.utils import timezone

class Organization(models.Model):
    owner = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='owned_organizations')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='organizations/', blank=True)
    members = models.ManyToManyField(to='accounts.User', through='OrganizationMembership', related_name='organizations')
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return '/static/images/default_organization_logo.jpg'

    def __str__(self):
        return self.name

class OrganizationMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher', 'Teacher'
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='organization_memberships')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.TEACHER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'user'], name='unique_organization_membership')
        ]

    def __str__(self):
        return f'{self.organization} - {self.user} - {self.role}'
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Seminar(models.Model):
    teacher = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='taught_seminars')
    organization = models.ForeignKey(to=Organization, on_delete=models.PROTECT, related_name='seminars', null=True, blank=True)
    participants = models.ManyToManyField(to='accounts.User', related_name='joined_seminars', blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    location = models.TextField()
    max_participants = models.PositiveBigIntegerField(blank=True, null=True)
    is_public = models.BooleanField()
    is_inperson = models.BooleanField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    image = models.ImageField(upload_to='seminar_image/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='seminars')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/default_seminar_image.png'

    @property
    def status(self):
        now = timezone.now()
        start = self.session_start
        end = self.session_end

        if now >= end:
            return 'completed'
        elif now < start:
            return 'upcoming'
        else:
            return 'inprogress'

    @property
    def progress(self):
        now = timezone.now()
        start = self.session_start
        end = self.session_end

        progress = (now - start) / (end - start) * 100
        return int(progress)

    def __str__(self):
        return self.title

class Review(models.Model):
    seminar = models.ForeignKey(to=Seminar, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seminar', 'user'], name='unique_user_seminar_review')
        ]