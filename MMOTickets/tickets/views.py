from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User
from .forms import TicketForm
from .models import Ticket, Responds
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect

# Create your views here.


class TicketsList(ListView):  # вьюшка для просмотра всех размещенных на сайте тикетов
    model = Ticket
    ordering = 'pubdate'
    template_name = 'tickets.html'
    context_object_name = 'tickets'


class UserTicketsList(ListView, LoginRequiredMixin):  # вьюшка для просмотра всех своих тикетов TODO страница доступна только для авторизованных
    model = Ticket
    ordering = 'pubdate'
    template_name = 'my_tickets.html'  # TODO копия основной страницы + кнопка редактировать тикет
    context_object_name = 'my_tickets'

    def get_queryset(self):
        return Ticket.objects.filter(author=self.request.user)


class UserRespondsList(ListView, LoginRequiredMixin):  # Вьюшка с откликами на свои тикеты TODO страница доступна только для авторизованных
    model = Responds
    ordering = 'ticket__pubdate'
    template_name = 'responds.html'  # TODO добавить кнопку для ответа респонденту (отправка майла)
    context_object_name = 'responds'

    def get_queryset(self):
        return Responds.objects.filter(ticket__author=self.request.user).prefetch_realted('head', 'category', )


@login_required
def ticket_detail(request, pk):  # вьюшка для редактирования тикетов
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if request.method == 'POST':
                if request.POST.get('response'):
                    if not Responds.objects.filter(ticket=dat, responder=request.user).exists():
                        Responds.objects.create(ticket=dat, responder=request.user)
                        return HttpResponseRedirect('/')
                    else:
                        form = TicketForm(instance=dat)
                        error = 'You already responded to that ticket'
                        context = {'data': data, 'form': form, 'error': error, 'dat': dat, }
                        return render(request, 'ticket_detail.html', context)
            else:
                form = TicketForm(instance=dat)
                context = {'data': data, 'form': form, 'dat': dat, }
                return render(request, 'ticket_detail.html', context)
    else:
        raise Http404


@login_required
def ticket_edit(request, pk):  # вьюшка для редактирования тикетов
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.author == request.user:
                if request.method == 'POST':
                    if request.POST.get('submit'):
                        form = TicketForm(request.POST, request.FILES, instance=dat)
                        if form.is_valid():
                            form.save()
                            return HttpResponseRedirect('/my_tickets/')
                    if request.POST.get('delete'):
                        dat.delete()
                        return HttpResponseRedirect('/')
                else:
                    form = TicketForm(instance=dat)
                    context = {'data': data, 'form': form, }
                    return render(request, 'ticket_edit.html', context)
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


@login_required
def ticket_responds(request, pk):
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if request.method == 'POST':
                if request.POST.get('delete'):
                    dat.delete()
                    return HttpResponseRedirect('my_tickets/')
            if dat.author == request.user:
                responds_qs = Responds.objects.filter(ticket=dat).prefetch_related('category', )
                context = {'responds': responds_qs, 'ticket': dat, }
                return render(request, 'ticket_responds.html', context)
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


@login_required
def ticket_create(request):  # вьюшка для создания тикетов
    form = TicketForm
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return HttpResponseRedirect('/')
    context = {'form': form, }
    return render(request, 'ticket_create.html', context)

