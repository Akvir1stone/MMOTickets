import random

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, OTCodeForm, LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from .models import OneTimeCode


# Create your views here.


class MyLoginView(LoginView):
    template_name = 'login.html'


def login_view(request):
    if request.POST.get('login'):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form = LoginForm()
                error = 'wrong username or password'
                context = {'form': form, 'error': error, }
                return render(request, 'login.html', context)
    if request.POST.get('registration'):
        return HttpResponseRedirect('/auth/registration/')
    form = LoginForm()
    context = {'form': form, }
    return render(request, 'login.html', context)


def registration_view(request):
    form = UserForm()
    print(1)
    if request.POST.get('send'):
        print(2)
        form = UserForm(request.POST)
        if form.is_valid():
            print(3)
            # user = User.objects.create_user(email=form.email, username=form.username, password=form.password)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            code = OneTimeCode.objects.create(code=random.randint(100000, 999999), username=username, email=email, password=password)
            code.save()
            # TODO send it to email
            return HttpResponseRedirect('/auth/code/')
        else:
            form = UserForm(request.POST)
            return render(request, 'registration.html', {'form': form, })
    return render(request, 'registration.html', {'form': form, })


def code_conformation_view(request):
    if request.method == 'POST':
        form = OTCodeForm(request.POST)
        if OneTimeCode.objects.filter(code=form.data['code']).exists():
            code_data = OneTimeCode.objects.filter(code=form.data['code'])
            for dat in code_data:
                user = User.objects.create_user(username=dat.username, email=dat.email, password=dat.password)
                user.save()
            return HttpResponseRedirect('/auth/login/')
    else:
        form = OTCodeForm()
        context = {'form': form, }
        return render(request, 'code.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
