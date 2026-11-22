from django.urls import path
from . import views
urlpatterns = [

    path('project1/daily-notes-monthly/', views.daily_notes_Monthly, name='daily_notes_monthly'),
    path('project1/daily-notes/', views.create_daily_note, name='create_daily_note'),
    path('project1/daily-notes/<int:note_id>/delete/',
         views.delete_daily_note, name='delete_daily_note'),
]
