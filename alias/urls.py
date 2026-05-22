from django.urls import path
from . import views

app_name = 'alias'

urlpatterns = [
    path('start/', views.start_alias_round, name='play'), 
    path('get-words/', views.get_next_word_api, name='get_words'),
]