from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import (
    Project,
    Milestone,
    Module,
    Task,
)


class ProjectListView(ListView):
    """
    Список проектов в которых участвует пользователь
    """
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    model = Project


class MilestonesLoaderView(View):

    def get(self, request, project_id):
        milestones = Milestone.objects.filter(project_id=project_id)

        context = {
            'milestones': milestones,
        }

        return render(request, 'project/_milestones-list.html', context)


class ModulesLoaderView(View):

    def get(self, request, milestone_id):
        modules = Module.objects.filter(milestone_id=milestone_id)

        context = {
            'modules': modules,
        }

        return render(request, 'project/_modules-list.html', context)


class TasksLoaderView(View):

    def get(self, request, module_id):
        tasks = Task.objects.filter(module_id=module_id)

        context = {
            'tasks': tasks,
        }

        return render(request, 'project/_tasks-list.html', context)


class SingleTaskLoaderView(View):

    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)

        context = {
            'task': task,
        }

        return render(request, 'project/_task.html', context)
