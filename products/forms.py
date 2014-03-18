__author__ = 'annalopatinski'
from django import forms
from .models import Profile
from .models import Product
from .models import Shop

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user",]

class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ['submitter',]


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['submitter',]

