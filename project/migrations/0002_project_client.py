# Generated by Django 2.0.6 on 2018-06-23 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Client', verbose_name='Клиент'),
        ),
    ]
