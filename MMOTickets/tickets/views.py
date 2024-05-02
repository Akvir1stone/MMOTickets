from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Category, Ticket

# Create your views here.


class TicketsList(ListView):
    model = Ticket
    ordering = 'pubdate'
    template_name = 'tickets.html'
    context_object_name = 'tickets'


class UserDetail(DetailView):
    model = User

# TODO UserTicketsList страница со своими тикетами метод с оповещением о респондах

# TODO UserRespondsList тикеты на которые дал респонд с оповещением о принятых респондах

# TODO UserDetail страница с основной информаией юзера принятыми респондами и открытыми тикетами

# TODO страницы регистрации и авторизации, подтверждение регистрации через почту

