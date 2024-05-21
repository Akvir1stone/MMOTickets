from django.db import models
from django.contrib.auth.models import User

from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

categories = {'tank': 'Танк', 'not a tank': 'не Танк', 'definetely not a tank': 'вообще не Танк', }
# class Category(models.Model):  # TODO возможно следует убрать эту модель и вместо нее
#     category_name = models.CharField(max_length=40)
#
#     def __str__(self):  # TODO Проверить действительно ли этот метот нужен
#         return self.category_name


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    head = models.CharField(max_length=200)
    body = CKEditor5Field('Text', config_name='extends')
    # category = models.ManyToManyField(Category, through='TicketCategory', related_name='tickets_category')
    category = models.CharField(choices=categories, max_length=25)
    pubdate = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)  # TODO убрать

    def close_ticket(self):
        self.status = False
        self.save()


# class TicketCategory(models.Model):
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Responds(models.Model):  # автоматическое определение респондера при создании
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
