# Generated by Django 5.0.4 on 2024-05-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_custom_auth', '0002_onetimecode_create_date_onetimecode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimecode',
            name='expire_time',
            field=models.DateTimeField(),
        ),
    ]