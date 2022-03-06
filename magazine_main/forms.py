from django import forms
from django.utils.translation import gettext as _

from .models import Item


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'amount_left']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_left': forms.TextInput(attrs={'class': 'form-control'}),
        }
