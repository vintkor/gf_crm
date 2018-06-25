from django.urls import path, include
from .views import (
    ProjectListView,
    MilestonesLoaderView,
    ModulesLoaderView,
    TasksLoaderView,
    SingleTaskLoaderView,
    AddCommentView,
)


app_name = 'project'
urlpatterns = [
    path('', ProjectListView.as_view(), name='user-projects-list'),
    path('load-milestones/<int:project_id>/', MilestonesLoaderView.as_view(), name='load-milestones'),
    path('load-modules/<int:milestone_id>/', ModulesLoaderView.as_view(), name='load-modules'),
    path('load-tasks/<int:module_id>/', TasksLoaderView.as_view(), name='load-tasks'),
    path('load-task/<int:task_id>/', SingleTaskLoaderView.as_view(), name='load-task'),
    path('add-comment-to-task/<int:task_id>/', AddCommentView.as_view(), name='add-comment-to-task'),
]
