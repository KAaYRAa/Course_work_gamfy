from django.urls import path
from . import views
app_name = 'crocodile'
urlpatterns = [
    path('play/', views.play_view, name='play'),
    path('get_words/', views.get_words, name='get_words'),
]