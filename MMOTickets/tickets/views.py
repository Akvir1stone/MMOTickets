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

# TODO нужна вьюшка (UserTicketsList) для просмотра и редактирования тикетов,
#  на ней размещены только те тикеты, которые были созданы текущим пользователем,
#  если их нет, то показывать предложение создать тикет


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
        return Responds.objects.filter(ticket__author=self.request.user)


class TicketDetail(DetailView):  # вьюшка для просмтора тикетов TODO нужно добавить кнопку респонда
    model = Ticket
    form = TicketForm
    # if request.method == 'POST':
    #     form = TicketForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form = TicketForm
    template_name = 'ticket_edit.html'  # TODO добавить свой темплейт
    context_object_name = 'ticket'


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
                            return HttpResponseRedirect('/')  # TODO перенаправлять на страницу моих тикетов
                    if request.POST.get('delete'):
                        dat.delete()
                        return HttpResponseRedirect('/')
                else:
                    form = TicketForm(instance=dat)
                    context = {'data': data, 'form': form, }  # 'pk': pk,
                    return render(request, 'ticket_edit.html', context)
            else:
                return HttpResponseForbidden()
    else:
        raise Http404


@login_required
def ticket_create(request):  # вьюшка для создания тикетов
    form = TicketForm
    if request.method == 'POST':
        form = TicketForm(request.POST)
        obj = form.save(commit=False)
        obj.author = request.user
        if obj.is_valid():
            obj.save()
            return HttpResponseRedirect('/')
    context = {'form': form, }
    return render(request, 'ticket_edit.html', context)


# TODO страницы регистрации и авторизации, подтверждение регистрации через почту


# class TicketCreate(LoginRequiredMixin, CreateView):
#     model = Ticket
#     form_class = TicketForm
#     success_url = "/"
#     template_name = "ticket_edit.html"
#     context_object_name = 'ticket_create'
