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
