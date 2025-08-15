# core/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import ToDo

@shared_task
def send_reminder_email(todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id)
        if todo.status == 'pending':
            subject = f"Reminder: {todo.task}"
            message = f"Your task '{todo.task}' is due on {todo.deadline.strftime('%Y-%m-%d %I:%M %p')}. Get it done!"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[todo.user.email],
                fail_silently=False,
            )
            print(f"Email sent for task '{todo.task}' to {todo.user.email}")
    except ToDo.DoesNotExist:
        print(f"Task {todo_id} not found, skipping email.")
    except Exception as e:
        print(f"Failed to send email for task {todo_id}: {str(e)}")