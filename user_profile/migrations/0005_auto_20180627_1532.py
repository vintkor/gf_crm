# Generated by Django 2.0.6 on 2018-06-27 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_client_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('order', models.CharField(default=10, max_length=200, verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Статус клиента',
                'verbose_name_plural': 'Статусы клиентов',
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_profile.ClientStatus', verbose_name='Статус'),
        ),
    ]