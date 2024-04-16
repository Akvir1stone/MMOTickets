from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=40)


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    head = models.CharField(max_length=200)
    body = 0  # TODO add django-ckeditor field
    category = models.ManyToManyField(Category, through='TicketCategory')
    responders = models.ManyToManyField(User, through='TicketResponders')


class TicketCategory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class TicketResponders(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
