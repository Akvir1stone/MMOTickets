# Generated by Django 5.0.4 on 2024-05-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='head',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
