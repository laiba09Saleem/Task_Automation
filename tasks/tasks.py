from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from tasks.models import TaskAssignment, Notifications
from django.core.mail import send_mail

@shared_task
def send_due_soon_notifications():
    now = timezone.now()

    soon = now + timedelta(hours=24)
    assignments = TaskAssignment.objects.filter(task__due_date__lte=soon, notified=False)
    for a in assignments:
        user = a.assignee
        task = a.task
        message = f"Reminder: Task '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}"

        Notifications.objects.create(user=user, message=message)

        try:
            send_mail(
                subject = f"Task Due Soon: {task.title}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            pass
        a.notified = True
        a.save()