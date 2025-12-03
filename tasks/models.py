from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, related_name='assignments', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'assignee')

class Notifications(models.Model):
    user = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)