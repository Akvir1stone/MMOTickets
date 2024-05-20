from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OneTimeCode(models.Model):
    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    code = models.CharField(max_length=6)
    # create_date = models.DateField(auto_now_add=True)

    def check_viability(self):  # TODO проверка времени прошедшего с создания вызов по таймеру раз в минуту, если время больше 'n', то удалить
        pass
