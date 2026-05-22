from django.urls import path
from . import views

app_name = 'never_have_i_ever'

urlpatterns = [
    path('play/', views.play_view, name='play'),
    
    path('get_data/', views.get_game_data, name='get_data'),
]