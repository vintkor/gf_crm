from django.contrib import admin
from .models import (
    Project,
    Status,
    Milestone,
    Module,
    Task,
    Comment,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'client',
        'pm',
        'status',
        'get_percent',
        'date_start',
        'date_end',
        'is_active',
        'created',
    )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'order',
    )
    list_editable = ('order',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'project',
        'index_number',
        'amount_of_days',
        'get_percent',
        'date_start',
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_editable = ('order',)
    save_on_top = True
    list_display = (
        'title',
        'milestone',
        'get_price',
        'get_percent',
        'order',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_editable = ('order', 'status')
    save_on_top = True
    list_display = (
        'title',
        'collaborator',
        'module',
        'get_price',
        'status',
        'order',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'created',
    )
