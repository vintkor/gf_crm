# Generated by Django 2.0.6 on 2018-07-24 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20180625_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Кол-во часов для выполнения'),
        ),
    ]
