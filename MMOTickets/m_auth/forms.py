from django import forms
from django.contrib.auth.models import User


class MyLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
