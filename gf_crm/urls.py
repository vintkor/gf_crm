from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from gf_crm.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include([
        path('', TemplateView.as_view(template_name='cabinet.html'), name='dashboard'),
        path('projects/', include('project.urls')),
    ])),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
