from django.urls import path, include
from .views import TicketsList, ticket_edit

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit),
]
