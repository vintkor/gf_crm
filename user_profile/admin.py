from django.contrib import admin
from .models import (
    User,
    Source,
    Client,
    ClientStatus,
    Developer,
    Technology,
    DeveloperTechnology,
)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'source',
    )


class ClientInline(admin.StackedInline):
    extra = 0
    model = Client


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_admin',
        'is_client',
    )
    readonly_fields = ('created', 'password')
    list_filter = ('is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    inlines = (ClientInline,)


@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    pass


class DeveloperTechnologyInline(admin.TabularInline):
    extra = 0
    model = DeveloperTechnology


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    inlines = (DeveloperTechnologyInline,)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    pass


@admin.register(DeveloperTechnology)
class DeveloperTechnologyAdmin(admin.ModelAdmin):
    pass
