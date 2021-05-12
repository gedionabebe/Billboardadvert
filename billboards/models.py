from django.db import models
#from accounts.models import Owner


class Billboard(models.Model):
    primary_photo = models.ImageField(upload_to='images/', default='default.png', blank=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey('accounts.Owner', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True)
    rating = models.IntegerField(default=0)
    rawrate = models.DecimalField(null=True,max_digits=30, decimal_places=5)
    rate_no = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    status = models.CharField(default="none", max_length=100)
# Create your models here.


class Advertisement(models.Model):
    photo = models.ImageField(default='default.png', blank=True)
    slogan = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    Advertiser = models.ForeignKey('accounts.Advertiser', on_delete=models.CASCADE)


class Request(models.Model):
    type = models.CharField(max_length=100)
    sender = models.ForeignKey('accounts.Account', related_name='sender', on_delete=models.CASCADE)
    to = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    status = models.CharField(default="none", max_length=100)


class Message(models.Model):
    sender = models.ForeignKey('accounts.Account', related_name='message_sender', on_delete=models.CASCADE)
    to = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    date = models.DateField()
    subject = models.CharField(default="none", max_length=100)
    body = models.CharField(default="none", max_length=100)


class Rent(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True)
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE)
    advertiser = models.ForeignKey('accounts.Advertiser', on_delete=models.CASCADE, default=None, null=True)