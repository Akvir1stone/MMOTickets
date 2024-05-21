from django.urls import path, include
from .views import TicketsList, ticket_edit, ticket_responds, ticket_create

urlpatterns = [
    path('', TicketsList.as_view()),
    path('ticket/<int:pk>/edit/', ticket_edit, name='ticket_edit'),
    path('ticket/<int:pk>/responds/', ticket_responds),
    # TODO create view with respond accept conformation
    path('create/', ticket_create),
]
