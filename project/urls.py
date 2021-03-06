from django.urls import path, include
from .views import (
    ProjectListView,
    MilestonesLoaderView,
    ModulesLoaderView,
    TasksLoaderView,
    SingleTaskLoaderView,
    AddCommentView,
    AddTaskFormView,
    AddModuleFormView,
    AddMilestoneFormView,
    AddProjectFormView,
    MakeTaskIsDoneView,
)


app_name = 'project'
urlpatterns = [
    path('', ProjectListView.as_view(), name='user-projects-list'),
    path('load-milestones/<int:project_id>/', MilestonesLoaderView.as_view(), name='load-milestones'),
    path('load-modules/<int:milestone_id>/', ModulesLoaderView.as_view(), name='load-modules'),
    path('load-tasks/<int:module_id>/', TasksLoaderView.as_view(), name='load-tasks'),
    path('load-task/<int:task_id>/', SingleTaskLoaderView.as_view(), name='load-task'),
    path('add-comment-to-task/<int:task_id>/', AddCommentView.as_view(), name='add-comment-to-task'),
    path('add-task/', AddTaskFormView.as_view(), name='add-task'),
    path('add-module/', AddModuleFormView.as_view(), name='add-module'),
    path('add-milestone/', AddMilestoneFormView.as_view(), name='add-milestone'),
    path('add-project/', AddProjectFormView.as_view(), name='add-project'),
    path('make-task-is-done/', MakeTaskIsDoneView.as_view(), name='make-task-is-done'),
]
