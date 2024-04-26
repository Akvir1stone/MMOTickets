from django.shortcuts import render
from django.views.generic import ListView
from .models import Category, Ticket

# Create your views here.


class TicketsList(ListView):
    model = Ticket

