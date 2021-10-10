from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.

class AccessLog(models.Model):
    SessionId = models.AutoField(primary_key=True)
    IpAddress = models.CharField(max_length = 50)
    QueryId = models.CharField(max_length = 20)
    FirstAccessed = models.DateTimeField(default=datetime.now)
    LastAccessed = models.DateTimeField(default=datetime.now)
    AddQuoteNum = models.IntegerField(default=0)
    PDFNum = models.IntegerField(default=0)
    XLSXNum = models.IntegerField(default=0)
    Mobile = models.BooleanField(default=False)

class QueryId_CompanyName(models.Model):
    QueryId = models.CharField(max_length = 20)
    CompanyName = models.CharField(max_length = 50)

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 35,unique=True)

    is_staff = models.BooleanField(('staff status'),default=False)
    is_superuser = models.BooleanField(('superuser status'),default=False)
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
