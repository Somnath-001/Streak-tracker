from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from core.tasks import send_reminder_email
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitEntry, ToDo
from django.utils import timezone


def reports(request):
    habits = Habit.objects.filter(user=request.user, is_deleted=False)
    completed_habits_all = Habit.objects.filter(user=request.user, is_completed=True, is_deleted=False)
    
    habit_data = []
    total_habits = habits.count()
    total_completed_days = 0
    total_possible_days = 0
    
    ongoing_habits_queryset = habits.filter(is_completed=False)
    for habit in ongoing_habits_queryset:
        total_days = habit.habitentry_set.count()
        completed_days = habit.habitentry_set.filter(completed=True).count()
        completion_rate = (completed_days / total_days * 100) if total_days > 0 else 0
        
        entries = habit.habitentry_set.order_by('date')
        streaks = []
        temp_streak = 0
        prev_date = None
        
        for entry in entries:
            if prev_date and (entry.date - prev_date).days > 1:
                if temp_streak > 0:
                    streaks.append(temp_streak)
                temp_streak = 0
            if entry.completed:
                temp_streak += 1
            elif temp_streak > 0:
                streaks.append(temp_streak)
                temp_streak = 0
            prev_date = entry.date
        if temp_streak > 0:
            streaks.append(temp_streak)
        
        highest_streak = max(streaks) if streaks else 0
        
        habit_data.append({
            'name': habit.name,
            'completion_rate': round(completion_rate, 1),
            'is_completed': habit.is_completed,
            'highest_streak': highest_streak,
        })
        total_completed_days += completed_days
        total_possible_days += total_days

    overall_completion_rate = (total_completed_days / total_possible_days * 100) if total_possible_days > 0 else 0
    ongoing_habits = ongoing_habits_queryset.count()
    completed_habits = completed_habits_all.count()

    # Expanded summary with more content, no notes link
    if total_habits == 0:
        summary = "No habits yet? Time to kickstart your journey! You’ve got zero habits to track—let’s change that. Imagine the streak you could build: studies say it takes 21 days to form a habit, so why not start today? Your future self is already cheering!"
    elif overall_completion_rate >= 75:
        summary = f"Rocking it! You’ve crushed {completed_habits}/{total_habits} habits with a stellar {round(overall_completion_rate, 1)}% consistency—pure legend status! With {ongoing_habits} habits still in play, you’ve logged {total_completed_days} days of wins out of {total_possible_days}. Fun fact: Consistency like yours beats 90% of New Year’s resolutions—keep that momentum roaring!"
    elif overall_completion_rate >= 50:
        summary = f"Solid moves! You’ve nailed {completed_habits}/{total_habits} habits, hitting {round(overall_completion_rate, 1)}% consistency—nice work! {ongoing_habits} habits are still rolling, with {total_completed_days}/{total_possible_days} days in the books. Did you know? Half the battle is showing up, and you’re doing it—turn those checks into a winning streak!"
    else:
        summary = f"Starting strong! {completed_habits}/{total_habits} habits are in the bag with {round(overall_completion_rate, 1)}% consistency—let’s crank it up! You’ve got {ongoing_habits} ongoing habits and {total_completed_days}/{total_possible_days} days tracked so far. Fun tidbit: Even a 1% daily boost compounds into epic gains—time to stack those victories!"

    milestones = []
    if total_habits > 0:
        if total_completed_days >= 10:
            milestones.append({'title': "10 Days Consistent", 'message': "You’ve checked off 10 days! Small steps lead to big wins—keep it up!", 'color': 'bg-info'})
        if total_completed_days >= 30:
            milestones.append({'title': "30-Day Champion", 'message': "Wow, 30 days of progress! You’re building habits like a pro!", 'color': 'bg-primary'})
        if any(h['highest_streak'] >= 7 for h in habit_data):
            milestones.append({'title': "Week-Long Warrior", 'message': "A 7-day streak? That’s serious dedication—stay unstoppable!", 'color': 'bg-warning'})
        if completed_habits >= 1:
            milestones.append({'title': "Habit Finisher", 'message': f"You’ve completed {completed_habits} habit{'' if completed_habits == 1 else 's'}! Celebrate your victory!", 'color': 'bg-success'})
        if any(h['completion_rate'] >= 100 for h in habit_data):
            milestones.append({'title': "Perfect Habit Master", 'message': "100% completion on a habit? You’re a perfectionist—amazing work!", 'color': 'bg-dark'})
        if any(h['completion_rate'] >= 90 for h in habit_data):
            milestones.append({'title': "Near-Perfect Achiever", 'message': "90%+ on a habit—almost flawless, keep shining!", 'color': 'bg-purple'})
        if any(h['completion_rate'] >= 75 for h in habit_data):
            milestones.append({'title': "Three-Quarter Titan", 'message': "75%+ completion—strong and steady, you’re crushing it!", 'color': 'bg-teal'})
        if any(h['completion_rate'] >= 50 for h in habit_data):
            milestones.append({'title': "Halfway Hero", 'message': "50%+ on a habit—half the battle won, keep pushing forward!", 'color': 'bg-orange'})
        if not milestones:
            milestones.append({'title': "First Steps", 'message': "Every journey starts somewhere—keep checking those boxes!", 'color': 'bg-secondary'})

    context = {
        'habit_data': habit_data,
        'overall_completion_rate': round(overall_completion_rate, 1),
        'summary': summary,
        'milestones': milestones,
        'total_completed_days': total_completed_days,
        'total_possible_days': total_possible_days,
    }
    return render(request, 'core/reports.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, Habit, HabitEntry
from datetime import datetime, timedelta, timezone

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

# Keep existing views like update_habit, reports, etc.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitEntry
from datetime import timedelta
from django.contrib import messages

@login_required
def habits(request, tab='all'):
    valid_tabs = ['ongoing', 'completed', 'deleted', 'all']
    if tab not in valid_tabs:
        tab = 'ongoing'

    if tab == 'ongoing':
        habits = Habit.objects.filter(user=request.user, is_deleted=False, is_completed=False)
    elif tab == 'completed':
        habits = Habit.objects.filter(user=request.user, is_deleted=False, is_completed=True)
    elif tab == 'deleted':
        habits = Habit.objects.filter(user=request.user, is_deleted=True)
    else:  # all
        habits = Habit.objects.filter(user=request.user)

    habits_with_rates = []
    for habit in habits:
        total_days = habit.habitentry_set.count()
        completed_days = habit.habitentry_set.filter(completed=True).count()
        completion_rate = (completed_days / total_days * 100) if total_days > 0 else 0
        habits_with_rates.append({
            'habit': habit,
            'completion_rate': round(completion_rate, 1)
        })

    if request.method == 'POST':
        name = request.POST['name']
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        habit = Habit.objects.create(user=request.user, name=name, start_date=start_date, end_date=end_date)
        current_date = start_date
        while current_date <= end_date:
            HabitEntry.objects.get_or_create(habit=habit, date=current_date, defaults={'completed': False})
            current_date += timedelta(days=1)
        messages.success(request, 'Habit added successfully!')
        return redirect('habits', tab=tab)

    return render(request, 'core/habits.html', {
        'habits_with_rates': habits_with_rates,
        'current_tab': tab,
        'today': timezone.now().date()  # Pass current date
    })

@login_required
def update_habit(request, habit_id, date):
    habit_entry = HabitEntry.objects.get(habit__id=habit_id, date=date, habit__user=request.user)
    habit_entry.completed = not habit_entry.completed
    habit_entry.save()
    messages.success(request, 'Habit entry updated!')
    return redirect('habits')

@login_required
def delete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    habit.is_deleted = True
    habit.save()
    messages.success(request, 'Habit deleted successfully!')
    return redirect('habits', tab='deleted')

@login_required
def complete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    habit.is_completed = True
    habit.save()
    messages.success(request, 'Habit marked as completed!')
    return redirect('habits', tab='completed')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitEntry, Note
from django.utils import timezone

@login_required
def notes(request):
    if request.method == "POST":
        title = request.POST.get('title')
        heading = request.POST.get('heading')
        content = request.POST.get('content')
        if title and heading and content:
            Note.objects.create(user=request.user, title=title, heading=heading, content=content)
            return redirect('notes')

    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notes': notes,
    }
    return render(request, 'core/notes.html', context)

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    note.delete()
    return redirect('notes')

# Rest of views (reports, etc.)...

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ToDo
from django.utils import timezone
from django.http import JsonResponse
from .tasks import send_reminder_email

@login_required
def to_do(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        task = request.POST.get('task')
        deadline_str = request.POST.get('deadline')
        reminder_str = request.POST.get('reminder')
        now = timezone.now().replace(second=0, microsecond=0)

        print(f"POST Data - Task: {task}, Deadline: {deadline_str}, Reminder: {reminder_str}, Now: {now}")

        if not all([task, deadline_str, reminder_str]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})

        try:
            deadline = timezone.datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            reminder = timezone.datetime.strptime(reminder_str, '%Y-%m-%dT%H:%M')
            deadline = timezone.make_aware(deadline, timezone.get_current_timezone())
            reminder = timezone.make_aware(reminder, timezone.get_current_timezone())

            print(f"Parsed - Deadline: {deadline}, Reminder: {reminder}")

            if deadline < now - timezone.timedelta(minutes=1) or reminder < now - timezone.timedelta(minutes=1):
                return JsonResponse({'success': False, 'error': 'Deadline and reminder must be within the last minute or future.'})

            todo = ToDo.objects.create(user=request.user, task=task, deadline=deadline, reminder=reminder)
            eta = max(0, (reminder - timezone.now()).total_seconds())
            send_reminder_email.apply_async((todo.id,), eta=eta)

            print(f"Task Created - ID: {todo.id}, Scheduled Reminder ETA: {eta} seconds")

            return JsonResponse({
                'success': True,
                'id': todo.id,
                'task': todo.task,
                'deadline': todo.deadline.strftime('%Y-%m-%d %I:%M %p'),
                'reminder': todo.reminder.strftime('%Y-%m-%d %I:%M %p'),
                'status': todo.status,
                'created_at': todo.created_at.strftime('%Y-%m-%d %I:%M %p')
            })
        except ValueError as e:
            print(f"ValueError: {e}")
            return JsonResponse({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM.'})
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {str(e)}'})

    todos = ToDo.objects.filter(user=request.user).order_by('deadline')
    context = {
        'todos': todos,
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M'),
    }
    return render(request, 'core/to_do.html', context)

@login_required
def update_todo_status(request, todo_id):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.status = 'completed' if todo.status == 'pending' else 'pending'
        todo.save()
        return JsonResponse({'success': True, 'status': todo.status})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def delete_todo(request, todo_id):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.delete()
        return JsonResponse({'success': True})
    return redirect('to_do')

# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')
