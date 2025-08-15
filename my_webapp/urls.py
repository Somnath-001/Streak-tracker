from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from core import views
from django.shortcuts import redirect
from my_webapp.settings import STATIC_ROOT

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # This includes login, logout, etc.
    path('', include('core.urls')),  # No namespace
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notes/', views.notes, name='notes'),
    path('habits/', views.habits, name='habits'),  # Default tab
    path('habits/<str:tab>/', views.habits, name='habits'),
    path('update_habit/<int:habit_id>/<str:date>/', views.update_habit, name='update_habit'),
    path('delete_habit/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('complete_habit/<int:habit_id>/', views.complete_habit, name='complete_habit'),
    path('reports/', views.reports, name='reports'),
] 