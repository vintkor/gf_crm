from django import forms
from django.utils.translation import ugettext as _
from .models import (
    Task,
    STATUS_CHOICES,
)
from user_profile.models import User


class AddTaskForm(forms.ModelForm):
    # module = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Заголовок задачи')
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label=_('Описание задачи')
    )
    collaborator = forms.ModelChoiceField(queryset=User.objects.all(), label=_('Исполнитель'), widget=forms.Select(
        attrs={'class': 'form-control select2'}
    ))
    time = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'step': '1'}),
        label=_('Время на задачу')
    )
    rate_per_hour = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'step': '1'}),
        label=_('Ставка в USD за 1 час')
    )
    status = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=STATUS_CHOICES),
        label=_('Статус задачи')
    )

    class Meta:
        model = Task
        fields = (
            'module',
            'title',
            'description',
            'collaborator',
            'time',
            'rate_per_hour',
            'status',
        )

    def __init__(self, *args, **kwargs):
        module_id = kwargs.pop('module_id')
        super().__init__(*args, **kwargs)
        self.fields['module'].initial = module_id
