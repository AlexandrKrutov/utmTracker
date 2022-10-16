from django.contrib import admin
from .models import UserName, UserProjects, ProjectsUTM, UTMTracker

# Register your models here.
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'project_name')

admin.site.register(UserProjects, UserProjectAdmin)

class UserNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name')

admin.site.register(UserName, UserNameAdmin)

class ProjectUTMsAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'utm_campaign', 'utm_source', 'utm_medium', 'utm_content', 'utm_term')

admin.site.register(ProjectsUTM, ProjectUTMsAdmin)

class UTMTrackerAdmin(admin.ModelAdmin):
    list_display = ('utm_campaign', 'date_time', 'event')

admin.site.register(UTMTracker, UTMTrackerAdmin)
