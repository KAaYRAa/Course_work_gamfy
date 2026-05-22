from django.urls import path
from . import views

app_name = 'dilemma'

urlpatterns = [
    path('play/', views.play_view, name='play'),
    path('get_data/', views.get_dilemmas, name='get_data'),
    path('vote/', views.vote_dilemma_api, name='vote_dilemma'), 
]