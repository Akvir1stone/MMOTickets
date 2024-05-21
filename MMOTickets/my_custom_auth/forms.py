from django import forms
from django.contrib.auth.models import User
from .models import OneTimeCode
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)


# class UserForm(UserCreationForm):
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password',)


class MyLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )


class OTCodeForm(forms.ModelForm):

    class Meta:
        model = OneTimeCode
        fields = ('code',)
