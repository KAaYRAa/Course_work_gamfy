from django.urls import path
from . import views

app_name = 'who_am_i'

urlpatterns = [

    path('play/', views.play_view, name='play'),

    path('get_characters/', views.get_characters, name='get_characters'),
]