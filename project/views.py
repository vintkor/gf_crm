import datetime
from django.template import Template, Context
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, FormView
from .models import (
    Project,
    Milestone,
    Module,
    Task,
    Comment)
from django.utils.translation import ugettext as _
from .forms import (
    AddTaskForm,
    AddModuleForm,
    AddMilestoneForm,
)


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
        if len(comment_text) > 0:

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

        return JsonResponse({
            'status': 0,
            'message': _('Комментарий не может быть пустым')
        })


class AddTaskFormView(FormView):
    """
    Добавление задачи
    """
    template_name = 'project/_add-task-modal.html'
    form_class = AddTaskForm
    module_id = None

    def get(self, *args, **kwargs):
        self.module_id = self.request.GET.get('module_id')
        return super(AddTaskFormView, self).get(args, kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddTaskFormView, self).get_form_kwargs()
        kwargs['module_id'] = self.module_id
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AddTaskFormView, self).get_context_data()
        context['module_id'] = self.module_id
        return context

    def post(self, request, *args, **kwargs):

        module_id = request.POST.get('module')
        title = request.POST.get('title')
        description = request.POST.get('description')
        collaborator_id = request.POST.get('collaborator')
        time = request.POST.get('time')
        rate_per_hour = request.POST.get('rate_per_hour')
        status = request.POST.get('status')

        task = Task(
            module_id=module_id,
            title=title,
            description=description,
            collaborator_id=collaborator_id,
            time=time,
            rate_per_hour=rate_per_hour,
            status=status,
        )
        task.save()
        context = {
            'task': task,
        }

        t = Template("{% include 'project/_task-part.html' with task=task %}")
        template = t.render(Context(context))

        module = task.module
        milestone = module.milestone
        project = milestone.project

        return JsonResponse({
            'status': 1,
            'template': template,
            'percentages': {
                'project': project.get_percent(),
                'project_id': project.id,
                'milestone': milestone.get_percent(),
                'milestone_id': milestone.id,
                'module': module.get_percent(),
                'module_id': module.id,
            }
        })

        # return render(request, 'project/_task-part.html', context)


class AddModuleFormView(FormView):
    """
    Добавление модуля
    """
    template_name = 'project/_add-module-modal.html'
    form_class = AddModuleForm
    milestone_id = None

    def get(self, *args, **kwargs):
        self.milestone_id = self.request.GET.get('milestone_id')
        return super(AddModuleFormView, self).get(args, kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddModuleFormView, self).get_form_kwargs()
        kwargs['milestone_id'] = self.milestone_id
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AddModuleFormView, self).get_context_data()
        context['milestone_id'] = self.milestone_id
        return context

    def post(self, request, *args, **kwargs):

        milestone_id = request.POST.get('milestone')
        title = request.POST.get('title')
        description = request.POST.get('description')

        module = Module(
            milestone_id=milestone_id,
            title=title,
            description=description,
        )
        module.save()
        context = {
            'module': module,
        }

        t = Template("{% include 'project/_module-part.html' with module=module %}")
        template = t.render(Context(context))

        milestone = module.milestone
        project = milestone.project

        return JsonResponse({
            'status': 1,
            'template': template,
            'percentages': {
                'project': project.get_percent(),
                'project_id': project.id,
                'milestone': milestone.get_percent(),
                'milestone_id': milestone.id,
            }
        })


class AddMilestoneFormView(FormView):
    """
    Добавление майлстоуна
    """
    template_name = 'project/_add-milestone-modal.html'
    form_class = AddMilestoneForm
    project_id = None

    def get(self, *args, **kwargs):
        self.project_id = self.request.GET.get('project_id')
        return super(AddMilestoneFormView, self).get(args, kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddMilestoneFormView, self).get_form_kwargs()
        kwargs['project_id'] = self.project_id
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AddMilestoneFormView, self).get_context_data()
        context['project_id'] = self.project_id
        return context

    def post(self, request, *args, **kwargs):

        project_id = request.POST.get('project')
        index_number = request.POST.get('index_number')
        amount_of_days = request.POST.get('amount_of_days')
        date_start = request.POST.get('date_start')

        milestone = Milestone(
            project_id=project_id,
            index_number=index_number,
            amount_of_days=amount_of_days,
            date_start=date_start,
        )
        milestone.save()
        context = {
            'milestone': milestone,
        }

        t = Template("{% include 'project/_milestone-part.html' with milestone=milestone %}")
        template = t.render(Context(context))

        project = milestone.project

        return JsonResponse({
            'status': 1,
            'template': template,
            'percentages': {
                'project': project.get_percent(),
                'project_id': project.id,
            }
        })
