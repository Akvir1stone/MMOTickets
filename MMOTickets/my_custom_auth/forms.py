from django import forms
from .models import OneTimeCode
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)


class MyLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )


class OTCodeForm(forms.ModelForm):

    class Meta:
        model = OneTimeCode
        fields = ('code',)
