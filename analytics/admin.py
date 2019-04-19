from django.contrib import admin
from .models import ObjectViewed, UserSession

def end_session(modeladmin, request, queryset):
    for user_session in queryset:
        user_session.end_session()
        
end_session.short_description = "Kill user session"

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'active', 'ended', 'timestamp',]
    ordering = ['-timestamp']
    actions = [end_session]

admin.site.register(ObjectViewed)
admin.site.register(UserSession, UserSessionAdmin)

