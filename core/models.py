from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Seminar(models.Model):
    teacher = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='taught_seminars')
    participants = models.ManyToManyField(to='accounts.User', related_name='joined_seminars', blank=True)
    # organizer = models.TextField(null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    location = models.TextField()
    is_public = models.BooleanField()
    is_inperson = models.BooleanField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    image = models.ImageField(upload_to='seminar_image/', blank=True)
    # max_particiant = models.CharField(max_length=7)
    # Platform
    # tag = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='seminars')
    created_at = models.DateTimeField(auto_now_add=True)
    # discount_code
    # is_course
    is_deleted = models.BooleanField(default=False)

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

# class Session(models.Model):
#     seminar = models.ForeignKey(to='core.Seminar', on_delete=models.CASCADE)
#     session_count = models.CharField(max_length=4)

# # class discription()