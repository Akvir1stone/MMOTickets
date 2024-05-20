from django.urls import path
from .views import TicketsList, ticket_edit, UserRespondsList, ticket_create, ticket_responds, UserTicketsList, ticket_detail

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit),
    path('ticket/<int:pk>', ticket_detail, name='ticket_detail'),
    path('responds/', UserRespondsList.as_view()),
    path('my_tickets/', UserTicketsList.as_view()),
    path('create/', ticket_create),
    path('ticket/<int:pk>/responds/', ticket_responds, name='ticket_responds'),
]
