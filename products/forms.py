__author__ = 'annalopatinski'
from django import forms
from .models import UserProfile
from .models import Product
from .models import Shop

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["submitter",]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["submitter",]

class OpenShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ['submitter',]


class AddproductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['submitter',]

