from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'first name...',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'last name...',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'username...',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(label=_('Password'), max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'password...',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password1',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ""

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user

