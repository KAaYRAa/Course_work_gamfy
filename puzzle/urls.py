from django.urls import path
from . import views

app_name = 'puzzle'

urlpatterns = [
    path('play/', views.play_view, name='play'),
    path('get_data/', views.get_puzzle_data, name='get_data'),
    path('check-guess/', views.check_puzzle_guess_api, name='check_guess'),
]