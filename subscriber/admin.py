from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'get_password_display', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email', 'name')
    readonly_fields = ('created_at', 'get_password_display')
    ordering = ('-created_at',)

    def get_password_display(self, obj):
        """Display decrypted password in admin"""
        return obj.get_password()
    get_password_display.short_description = 'Password'

    fieldsets = (
        ('User Information', {
            'fields': ('email', 'name')
        }),
        ('Security', {
            'fields': ('get_password_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
