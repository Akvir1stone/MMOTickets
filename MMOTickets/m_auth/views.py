import random

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import MyLoginForm
from django.http import HttpResponseRedirect

# Create your views here.


def login_view(request):
    form = MyLoginForm()
    if request.POST.get('login'):
        form = MyLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.data['email'], password=form.data['password'], )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('')
            else:
                form = MyLoginForm()
                error = 'wrong email or password'
                context = {'form': form, 'error': error, }
                return render(request, 'login.html', context)
    if request.POST.get('registration'):
        return HttpResponseRedirect('auth/registration/')
    context = {'form': form, }
    return render(request, 'login.html', context)


# TODO code = OneTimeCode.objects.create(code=random.randint(100000, 999999), username=form.data['username'], email=form.data['email'], password=form.data['password'])
