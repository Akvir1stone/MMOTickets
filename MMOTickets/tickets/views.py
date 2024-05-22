from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
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


@login_required
def ticket_responds(request, pk):
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.author == request.user:
                responds_qs = Responds.objects.filter(ticket=dat)  # TODO prefetch_related and also do that for UserRespondsList
                context = {'responds': responds_qs, }
                return render(request, 'ticket_responds.html', context)
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


class UserTicketsList(ListView, LoginRequiredMixin):  # вьюшка для просмотра всех своих тикетов TODO страница доступна только для авторизованных
    model = Ticket
    ordering = 'pubdate'
    template_name = 'my_tickets.html'  # TODO копия основной страницы + кнопка редактировать тикет
    context_object_name = 'my_tickets'

    def get_queryset(self):
        return Ticket.objects.filter(author=self.request.user)


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
def ticket_create(request):  # вьюшка для создания тикетов
    if request.method == 'POST':
        if request.POST.get('submit'):
            form = TicketForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.author = request.user
                obj.save()
                return HttpResponseRedirect('/')
    else:
        form = TicketForm
        context = {'form': form, }
        return render(request, 'ticket_create.html', context)


@login_required
def respond_conformation(request, pk):
    data = Responds.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.ticket.author == request.user:
                dat.is_accepted = True
                # TODO send mail to responder (dat.responder.email)
                return HttpResponseRedirect('/my_tickets')
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


@login_required
def respond_delete(request, pk):
    data = Responds.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.ticket.author == request.user:
                dat.delete()
                return HttpResponseRedirect('/my_tickets')
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


@login_required
def ticket_delete(request, pk):
    data = Ticket.objects.filter(pk=pk)
    if data:
        for dat in data:
            if dat.author == request.user:
                dat.delete()
                return HttpResponseRedirect('/my_tickets')
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


