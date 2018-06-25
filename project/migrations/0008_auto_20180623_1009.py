# Generated by Django 2.0.6 on 2018-06-23 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_module_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='rate_per_hour',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Ставка за час (USD)'),
        ),
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.PositiveSmallIntegerField(default=25, verbose_name='Кол-во часов для выполнения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='collaborator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]