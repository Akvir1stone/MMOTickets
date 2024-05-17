from django.urls import path, include
from .views import TicketsList, ticket_edit, ticket_responds

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit),
    #  TODO new
    path('ticket/<int:pk>/responds/', ticket_responds),
]
