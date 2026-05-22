from django.shortcuts import render, redirect
from .forms import ExistingUserRegisterForm
from django.contrib import messages
from .models import Users
from games.models import FavoriteGame, Games
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from games.models import GameSession, Games
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def register_view(request):
    if request.method == 'POST':
        form = ExistingUserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            user.password_hash = make_password(form.cleaned_data['password']) 
            user.save()
            
            messages.success(request, 'Реєстрація успішна! Тепер увійдіть.')
            return redirect('users:login')
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ExistingUserRegisterForm()
        
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(username=username)
            
            if check_password(password, user.password_hash):

                request.session['user_id'] = user.id 
                messages.success(request, f'Вітаємо, {user.username}!')
                return redirect('games:home')  
            else:
                messages.error(request, 'Невірний пароль!')
        except Users.DoesNotExist:
            messages.error(request, 'Користувача не знайдено!')
            
    return render(request, 'users/login.html')


def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('users:login')

    user_id = request.session['user_id']
    favorite_list = []
    current_user = None

    try:
        current_user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return redirect('users:login')


    if request.method == 'POST':
 
        new_username = request.POST.get('username')
        if new_username:
            current_user.username = new_username

    
        if 'avatar' in request.FILES: 
            current_user.avatar = request.FILES['avatar']
            
        current_user.save()
        messages.success(request, 'Профіль успішно оновлено!')
        return redirect('users:profile') 


    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT g.id, g.name 
                FROM "user_favorites" f
                JOIN "games" g ON f.game_id = g.id
                WHERE f.user_id = %s
            """, [user_id])
            
            rows = cursor.fetchall()

            for row in rows:
                game_id, game_name = row
                
                game_url = "#"
                if game_id == 10:   game_url = reverse('crocodile:play')
                elif game_id == 8:  game_url = reverse('never_have_i_ever:play')
                elif game_id == 7:  game_url = reverse('danetki:play')
                elif game_id == 9:  game_url = reverse('dilemma:play')
                elif game_id == 4:  game_url = reverse('who_am_i:play')
                elif game_id == 5:  game_url = reverse('puzzle:play')
                elif game_id == 6:  game_url = reverse('five_seconds:play')
                elif game_id == 1:  game_url = reverse('games:game_detail', args=[1])

                favorite_list.append({
                    'id': game_id,
                    'title': game_name,
                    'name': game_name,
                    'url': game_url,
                })
        except Exception as e:
            print(f"Помилка SQL в кабінеті: {str(e)}")

    context = {
        'favorite_games': favorite_list,
        'user': current_user
    }
    return render(request, 'users/profile.html', context)

def logout_view(request):

    logout(request) 
    return redirect('users:login')


def user_history(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('users:login')
    
    user_obj = Users.objects.get(id=user_id)
    history = GameSession.objects.filter(user=user_obj).order_by('-start_time')

    games_map = {g.id: g.title for g in Games.objects.all()}


    for session in history:
        session.game_name = games_map.get(session.game_id, "Невідома гра")

    return render(request, 'users/history.html', {'history': history})

def search_users_view(request):
    query = request.GET.get('user_search', '')
    found_users = []
    if query:

        found_users = Users.objects.filter(username__icontains=query)
    return render(request, 'users/search_results.html', {'users': found_users, 'query': query})

def public_profile_view(request, target_user_id):
    if 'user_id' in request.session and request.session['user_id'] == target_user_id:
        return redirect('users:profile')

    favorite_list = []
    target_user = None

    try:
        target_user = Users.objects.get(id=target_user_id)
    except Users.DoesNotExist:
        return redirect('games:home')

    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT g.id, g.name 
                FROM "user_favorites" f
                JOIN "games" g ON f.game_id = g.id
                WHERE f.user_id = %s
            """, [target_user_id])
            
            rows = cursor.fetchall()

            for row in rows:
                game_id, game_name = row
                
                game_url = "#"
                if game_id == 10:   game_url = reverse('crocodile:play')
                elif game_id == 8:  game_url = reverse('never_have_i_ever:play')
                elif game_id == 7:  game_url = reverse('danetki:play')
                elif game_id == 9:  game_url = reverse('dilemma:play')
                elif game_id == 4:  game_url = reverse('who_am_i:play')
                elif game_id == 5:  game_url = reverse('puzzle:play')
                elif game_id == 6:  game_url = reverse('five_seconds:play')
                elif game_id == 1:  game_url = reverse('games:game_detail', args=[1])

                favorite_list.append({
                    'id': game_id,
                    'name': game_name,
                    'title': game_name,  
                    'url': game_url,
                })
        except Exception as e:
            print(f"Помилка SQL в публічному кабінеті: {str(e)}")

    context = {
        'target_user': target_user,
        'favorite_games': favorite_list,
    }
    return render(request, 'users/public_profile.html', context)

def public_user_history_view(request, target_user_id):

    try:
        user_obj = Users.objects.get(id=target_user_id)
    except Users.DoesNotExist:
        return redirect('games:home')
    

    history = GameSession.objects.filter(user=user_obj).order_by('-start_time')


    games_map = {g.id: g.title for g in Games.objects.all()}

    for session in history:
        session.game_name = games_map.get(session.game_id, "Невідома гра")

    context = {
        'history': history,
        'target_user': user_obj
    }
    return render(request, 'users/public_history.html', context)