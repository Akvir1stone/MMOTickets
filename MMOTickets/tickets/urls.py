from django.urls import path, include
from .views import TicketsList, ticket_edit, UserRespondsList, ticket_create

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit),
    path('responds/', UserRespondsList.as_view()),
    path('create/', ticket_create),
]
