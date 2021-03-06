from django import forms
from django.utils.translation import ugettext as _
from .models import (
    Task,
    Module,
    Milestone,
    Project,
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label=_('Описание задачи')
    )
    collaborator = forms.ModelChoiceField(queryset=User.objects.all(), label=_('Исполнитель'), widget=forms.Select(
        attrs={'class': 'form-control select2'}
    ))
    time = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'step': '1', 'value': 1}),
        label=_('Время на задачу'), required=False
    )
    rate_per_hour = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'step': '1', 'value': 1}),
        label=_('Ставка в USD за 1 час'), required=False
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


class AddModuleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Заголовок задачи')
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label=_('Описание задачи')
    )

    class Meta:
        model = Module
        fields = (
            'milestone',
            'title',
            'description',
        )

    def __init__(self, *args, **kwargs):
        milestone_id = kwargs.pop('milestone_id')
        super().__init__(*args, **kwargs)
        self.fields['milestone'].initial = milestone_id


class AddMilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = (
            'project',
            'index_number',
            'amount_of_days',
            'date_start',
        )

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id')
        super().__init__(*args, **kwargs)
        self.fields['project'].initial = project_id


class AddProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'client',
            'pm',
            'status',
            'is_active',
            'date_start',
            'date_end',
        )
