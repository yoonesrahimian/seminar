from django.db import models

class Seminar(models.Model):
    teacher = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='teacher')
    participants = models.ManyToManyField(to='accounts.User', related_name='participant', blank=True)
    # organizer = models.TextField(null=True)
    title = models.CharField(max_length=50)
    discription = models.TextField()
    price = models.PositiveIntegerField()
    location = models.TextField()
    is_public = models.BooleanField()
    is_inperson = models.BooleanField()
    session_date = models.DateField()
    session_time_start = models.TimeField()
    session_time_end = models.TimeField()
    image = models.ImageField(upload_to='seminar_image/', null=True)
    # max_particiant = models.CharField(max_length=7)
    # Platform
    # hashtag = models.TextField()
    # category
    # discount_code
    # is_course

# class Session(models.Model):
#     seminar = models.ForeignKey(to='core.Seminar', on_delete=models.CASCADE)
#     session_count = models.CharField(max_length=4)

# # class discription()