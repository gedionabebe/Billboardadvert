from django import forms
from .models import Account
"""

class RegisterAnAccount(forms.Form):
    #profilePicture = forms.ImageField(label="Image")
    name = forms.CharField(max_length=100,label="Name")
    phoneNumber = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=100, label="Password")


"""


class RegisterUserForm(forms.Form):
    # profile_picture = forms.ImageField()
    name = forms.CharField(max_length=100)
    phone_number = forms.IntegerField()
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    Account_type = forms.CharField(max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(max_length=100, label="Password")



class AddAdvertisementForm(forms.Form):
    # photo = forms.ImageField(default='default.png', blank=True)
    slogan = forms.CharField(label="Slogan", max_length=200)
    description = forms.CharField(label="Description", max_length=200)


INTEGER_CHOICES = [tuple([x,x]) for x in range(1,6)]

class rateForm(forms.Form):
    rating = forms.IntegerField(widget=forms.Select(choices=INTEGER_CHOICES))
