# Generated by Django 2.0.6 on 2018-06-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
