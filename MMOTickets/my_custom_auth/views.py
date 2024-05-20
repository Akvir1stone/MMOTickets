import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from .models import OneTimeCode
from .forms import OTCodeForm, UserForm, MyLoginForm

# Create your views here.


def registration_view(request):
    form = UserForm()
    if request.POST.get('send'):
        form = UserForm(request.POST)
        if form.is_valid():
            # user = User.objects.create_user(email=form.email, username=form.username, password=form.password)
            code = OneTimeCode.objects.create(code=random.randint(100000, 999999), username=form.data['username'], email=form.data['email'], password=form.data['password'])
            code.save()
            # TODO send it to email
            return HttpResponseRedirect('/auth/code/')
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


def login_view(request):
    if request.POST.get('login'):
        form = MyLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.data['email'], password=form.data['password'], )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form = MyLoginForm()
                error = 'wrong email or password'
                context = {'form': form, 'error': error, }
                return render(request, 'login.html', context)
    if request.POST.get('registration'):
        return HttpResponseRedirect('/auth/registration/')
    form = MyLoginForm()
    context = {'form': form, }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
