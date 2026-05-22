from django.urls import path
from . import views 

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.user_history, name='user_history'),
    path('search/', views.search_users_view, name='search_users'),
    path('profile/<int:target_user_id>/', views.public_profile_view, name='public_profile'), 
    path('profile/<int:target_user_id>/history/', views.public_user_history_view, name='public_user_history'),  
]