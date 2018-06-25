import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import (
    Project,
    Milestone,
    Module,
    Task,
    Comment)
from django.utils.translation import ugettext as _


class ProjectListView(ListView):
    """
    Список проектов в которых участвует пользователь
    """
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    model = Project

    def get(self, *args, **kwargs):
        last_visited_task = self.request.COOKIES.get('last_visited_task')

        if last_visited_task:
            try:
                task = Task.objects.get(id=last_visited_task)
            except Task.DoesNotExist:
                return super(ProjectListView, self).get(args, kwargs)

            module = task.module
            milestone = module.milestone
            project = milestone.project

            context = {
                'current_module': module,
                'modules': milestone.module_set.all(),
                'current_milestone': milestone,
                'milestones': project.milestone_set.all(),
                'current_task': task,
                'tasks': module.task_set.all(),
                'current_project': project,
                self.context_object_name: self.get_queryset(),
                'has_last_visited_task': True,
            }

            return render(self.request, self.template_name, context)

        return super(ProjectListView, self).get(args, kwargs)


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


class AddCommentView(View):
    """
    Добавление коментария к задаче
    """

    def post(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseBadRequest()

        comment_text = request.POST.get('comment_text')

        comment = Comment(
            text=comment_text,
            user=self.request.user,
            task=task,
        )
        comment.save()

        context = {
            'comment': comment,
        }

        return render(request, 'project/_comment.html', context)


class AddTaskView(View):

    def get(self, request):
        context = {}
        return render(request, 'project/_add-task-modal.html', context)
