import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from domains.managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    account = models.ForeignKey("domains.Account", on_delete=models.CASCADE, db_column="account_id", default=None, null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Account(models.Model):
    STATUS_CHOICES = (
        ('1', 'Pending'),
        ('2', 'Verified'),
        ('3', 'Disabled'),
        ('4', 'Deleted')
    )
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_prefix_id = models.CharField(max_length=6, unique=True)
    account_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    domain_cap = models.IntegerField(default=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default='1')

    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name_plural = "Accounts"

class Domain(models.Model):
    SOURCE_TYPE_CHOICES = (
        ('1', 'DNS'),
        ('2', 'DB'),
        ('3', 'Mirror')
    )
    STATUS_CHOICES = (
        ('1', 'Pending'),
        ('2', 'Verified'),
        ('3', 'Disabled'),
        ('4', 'Deleted'),
        ('5', 'Enabled'),
    )
    domain_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    domain_name = models.CharField(max_length=255)
    source_prefix = models.CharField(max_length=8, unique=True)
    source_type = models.CharField(choices=SOURCE_TYPE_CHOICES, max_length=255, default='1')
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default='1')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.domain_name
