from django.contrib import admin
from .models import (
    Status,
    User,
    Source,
    Client,
)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


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
        'rate_per_hour',
        'is_admin',
        'is_client',
    )
    readonly_fields = ('created', 'password')
    list_filter = ('is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    inlines = (ClientInline,)
