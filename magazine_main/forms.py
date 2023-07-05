from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from .models import Item, Borrowed


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'amount_left']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_left': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BorrowItemForm(forms.ModelForm):
    class Meta:
        model = Borrowed
        fields = ['user', 'item', 'amount']
