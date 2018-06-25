from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from gf_crm.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include([
        path('', TemplateView.as_view(template_name='cabinet.html'), name='dashboard'),
        path('projects/', include('project.urls')),
    ])),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
