from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)  # New: Tracks if habit is completed
    is_deleted = models.BooleanField(default=False)    # New: Tracks if habit is deleted

    def __str__(self):
        return self.name

class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    reminder = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"{self.task} (Due: {self.deadline.strftime('%Y-%m-%d %H:%M')})"

# Existing Note, Habit, HabitEntry models...