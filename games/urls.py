from django.urls import path

from . import views 

app_name = 'games'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('favorite/toggle/<int:game_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('save_result/', views.save_game_result, name='save_result'),
]