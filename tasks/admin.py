from django.contrib import admin
from tasks.models import Task, TaskAssignment, Notifications

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','created_by','status','due_date','created_at')
    search_fields = ('title','created_by__username')

admin.site.register(TaskAssignment)
admin.site.register(Notifications)