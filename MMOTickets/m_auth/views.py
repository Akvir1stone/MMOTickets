from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import MyLoginForm

# Create your views here.


def login_view(request):
    form = MyLoginForm()
    if request.POST.get('login'):
        form = MyLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.data['email'], password=form.data['password'], )
            if user is not None:
                pass  # TODO login
            else:
                pass  #
    context = {'form': form,}
    return render(request, 'login.html', context)
