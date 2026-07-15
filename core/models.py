from django.db import models
from datetime import datetime

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
    session_date = models.DateField()
    session_time_start = models.TimeField()
    session_time_end = models.TimeField()
    image = models.ImageField(upload_to='seminar_image/', blank=True)
    # max_particiant = models.CharField(max_length=7)
    # Platform
    # hashtag = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="seminars")
    # discount_code
    # is_course

    @property
    def status(self):
        today = datetime.now().today()
        now = datetime.combine(today, datetime.now().time().replace(microsecond=0))
        start = datetime.combine(today, self.session_time_start)
        end = datetime.combine(today, self.session_time_end)

        if now < start:
            return "upcoming"
        elif now >= end:
            return "completed"
        else:
            return "inprogress"

    @property
    def progress(self):
        today = datetime.now().today()
        now = datetime.combine(today, datetime.now().time().replace(microsecond=0))
        start = datetime.combine(today, self.session_time_start)
        end = datetime.combine(today, self.session_time_end)

        progress = (now - start) / (end - start) * 100
        return int(progress)

# class Session(models.Model):
#     seminar = models.ForeignKey(to='core.Seminar', on_delete=models.CASCADE)
#     session_count = models.CharField(max_length=4)

# # class discription()