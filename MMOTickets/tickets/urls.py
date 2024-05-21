from django.urls import path, include
from .views import TicketsList, ticket_edit, ticket_responds, ticket_create, respond_conformation, respond_delete

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit, name='ticket_edit'),
    path('ticket/<int:pk>/responds/', ticket_responds),
    path('respond/<int:pk>/confirm/', respond_conformation, name='respond_conformation'),
    path('respond/<int:pk>/delete/', respond_delete, name='respond_delete'),
    path('create/', ticket_create),
]
