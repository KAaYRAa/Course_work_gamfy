from django.urls import path
from . import views

app_name = 'danetki'

urlpatterns = [
    path('play/', views.play_view, name='play'),
    path('get_data/', views.get_danetka, name='get_data'),
]