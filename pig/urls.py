from django.urls import path
from . import views

app_name = 'pig'

urlpatterns = [
    path('play/', views.pig_play_view, name='play'),
    
    path('get_task/', views.get_random_task, name='get_task'),
    path('add-letter/', views.add_letter_post_api, name='add_letter'),
]