from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from core.models import Organization, OrganizationMembership

COUNTRY_CHOICES = [
    ("IR", "Iran"),
    ("TR", "Turkey"),
    ("AZ", "Azerbaijan"),
]

CITY_CHOICES = [
    ("TEH", "Tehran"),
    ("TBZ", "Tabriz"),
    ("MSH", "Mashhad"),
]

class User(AbstractUser):
    phone = PhoneNumberField(null=True, unique=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=3, choices=CITY_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    biography = models.CharField(max_length=255, blank=True)
    favorite_seminars = models.ManyToManyField(to='core.Seminar', related_name='favorited_by', blank=True)

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default_profile_picture.jpg'

    def __str__(self):
        return self.username

class OrganizationInvitation(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE, related_name='invitations')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='organization_invitations')
    role = models.CharField(max_length=30, choices=OrganizationMembership.Role.choices)
    status = models.CharField(max_length=30, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'organization'],
                condition=models.Q(status='pending'),
                name='unique_pending_organization_invitation',
                )
        ]

    def __str__(self):
        return f'from {self.organization} to {self.user} ({self.status})'

class Notification(models.Model):
    class NotificationTypeChoices(models.TextChoices):
        NORMAL = 'normal', 'Normal'
        INVITATION = 'invitation', 'Invitation'
        ADVERTISEMENTS = 'ads', 'Advertisements'
    recipient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    related_seminar = models.ForeignKey(to='core.Seminar', on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    invitation = models.ForeignKey(to=OrganizationInvitation, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationTypeChoices.choices, default=NotificationTypeChoices.NORMAL)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.recipient.username} - {self.title}'

class Wallet(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    def __str__(self):
        return f'{self.user}'

class WalletTransaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'deposit', 'Deposit'
        SEMINAR_PAYMENT = 'seminar_payment', 'Seminar Payment'
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wallet.user} - {self.transaction_type} - {self.amount}'