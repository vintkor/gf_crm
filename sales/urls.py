from django.urls import path, include
from .views import (
    ClientsListView,
)


app_name = 'sales'
urlpatterns = [
    path('', ClientsListView.as_view(), name='clients-list'),
]
