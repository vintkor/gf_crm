from django.shortcuts import render
from django.views.generic import ListView
from user_profile.models import Client


class ClientsListView(ListView):
    template_name = 'sales/clients-list.html'
    context_object_name = 'clients'
    model = Client
