from django.urls import path
from . import views

urlpatterns = [
    path('https://streak-tracker-a0da.onrender.com', views.home, name='home'),
    path('habits/<str:tab>/', views.habits, name='habits'),  # Changed 'status' to 'tab'
    # path('habits/add/', views.add_habit, name='add_habit'),
    # path('habits/edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('habits/delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('habits/complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),
    # path('entry/<int:habit_id>/<str:date>/', views.toggle_entry, name='toggle_entry'),
    path('reports/', views.reports, name='reports'),
    path('notes/', views.notes, name='notes'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('to-do/', views.to_do, name='to_do'),
    path('to-do/<int:todo_id>/update/', views.update_todo_status, name='update_todo_status'),
    path('to-do/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]

