from django import template
from project.models import Task

register = template.Library()


@register.inclusion_tag('project/_add-comment-form.html')
def add_comment(user, task):
    if task.collaborator == user or task.module.milestone.project.pm == user:
        return {'can_add_comment': True, 'task': task}
    return {'can_add_comment': False}


# @register.simple_tag
# def can_add_comment(user, task):
#     pass