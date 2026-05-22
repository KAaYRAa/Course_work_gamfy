from django.urls import path
from . import views

app_name = 'mafia'

urlpatterns = [
    path('rules/', views.mafia_rules_view, name='rules'),
    path('play/', views.mafia_play_view, name='play'),
    path('distribute_roles/', views.distribute_roles_api, name='distribute_roles'),
    path('get_my_role/', views.get_my_role_api, name='get_my_role'),
    path('eliminate_player/', views.eliminate_player_api, name='eliminate_player'),
]