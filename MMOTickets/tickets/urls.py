from django.urls import path, include
from .views import TicketsList

urlpatterns = [
    path('', TicketsList.as_view()),
]
