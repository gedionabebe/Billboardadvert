from django.db import models
from billboards.models import *
from django.contrib.auth.models import User


class Account(models.Model):
    # profile_picture = models.ImageField(default='default.png', blank=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField(default='noemail@empty.com')
    password = models.CharField(max_length=100)
    Account_type = models.CharField(max_length=100)
    rating = models.IntegerField()
    def __str__(self):
        return self.name + '--' + self.password + '--' + self.Account_type


class Advertiser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    rented_billboards = models.CharField(max_length=100)


class Owner(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    preferred_content = models.CharField(max_length=100)


class Administrator(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)