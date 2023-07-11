from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from .models import Item, Borrowed, ItemType


class AddItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'serial_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['type', 'name', 'serial_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
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
    def __init__(self, *args, **kwargs):
        super (BorrowItemForm,self).__init__(*args,**kwargs)
        self.fields['item'].queryset = Item.objects.filter(borrowed=False)

    class Meta:
        model = Borrowed
        fields = ['user', 'item', 'amount']
