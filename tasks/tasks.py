from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(completed=False, due_date__lte=timezone.now())

    for task in tasks:
        send_mail(
            '⏰ Task Reminder',
            f'Task "{task.title}" is due now!',
            'from@example.com',
            [task.user.email],
        )