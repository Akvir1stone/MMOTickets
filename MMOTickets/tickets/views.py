from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from .forms import TicketForm
from .models import Ticket, Responds

# Create your views here.


class TicketsList(ListView):  # вьюшка для просмотра всех размещенных на сайте тикетов
    model = Ticket
    ordering = 'pubdate'
    template_name = 'tickets.html'
    context_object_name = 'tickets'

# TODO нужна вьюшка (MyTicketsView) для просмотра и редактирования тикетов,
#  на ней размещены только те тикеты, которые были созданы текущим пользователем,
#  если их нет, то показывать предложение создать тикет


class UserRespondsList(DetailView):  # уже сделано
    pass


class TicketDetail(DetailView):  # вьюшка для просмтора тикетов TODO нужно добавить кнопку респонда
    model = Ticket
    form = TicketForm
    # if request.method == 'POST':
    #     form = TicketForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form = TicketForm
    template_name = 'ticket_edit.html'
    context_object_name = 'ticket'


def ticket_edit(request, pk):  # вьюшка для редактирования тикетов
    data = Ticket.objects.filter(pk=pk)  # TODO сделать кнопку сохранения и возврата на строницу MyTicketsView
    if data:  # TODO добавить else который будет возвращать ошибку 404
        form = TicketForm  # TODO сделать кнопку удаления тикета и возврата на строницу MyTicketsView
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                form.save()
                form = TicketForm
        context = {'data': data, 'form': form, }  # 'pk': pk,
        return render(request, 'ticket_edit.html', context)


@login_required  # TODO new
def ticket_responds(request, pk):
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.author == request.user:
                responds_qs = Responds.objects.filter(ticket=dat)
                context = {'responds': responds_qs, }
                return render(request, 'ticket_responds.html', context)
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


# TODO UserTicketsList страница со своими тикетами метод с оповещением о респондах

# TODO страница просмотра респодов с кнопкой ответа на них и оповещением респондента

# TODO UserRespondsList тикеты на которые дал респонд с оповещением о принятых респондах

# TODO страницы регистрации и авторизации, подтверждение регистрации через почту

