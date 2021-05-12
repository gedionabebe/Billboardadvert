from django import forms
from .models import Advertisement

class AddBillboardForm(forms.Form):
    photo = forms.ImageField()
    name = forms.CharField(label="Name", max_length=200)
    location = forms.CharField(label="loaction", max_length=200)
    price = forms.IntegerField()
    length = forms.IntegerField()
    width = forms.IntegerField()
class RentRequestForm(forms.Form):
    startDate = forms.DateField()
    endDate = forms.DateField()
    advertisementType = forms.CharField(label="Advertisement", max_length=200)

#copy this

Price_Range=[
    ('budget','Budget'),
    ('midrange','Midrange'),
    ('uppermidrange','Upper Midrange'),
    ('highend','High End'),
]
Size_Range=[
    ('small','Small'),
    ('medium','Medium'),
    ('large','Large'),
    ('extralarge','Extra Large')
    ]
class FilterForm(forms.Form):
    price_range=forms.CharField(label='Choose your price range.', widget=forms.Select(choices=Price_Range))
    size_range=forms.CharField(label='Choose your size range.', widget=forms.Select(choices=Size_Range))

#till here