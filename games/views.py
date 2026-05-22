from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

from .models import Games, FavoriteGame, GameSession
from users.models import Users

def home_view(request):
    search_query = request.GET.get('search', '')
    players_count = request.GET.get('players')
    games_list = Games.objects.all()

    if search_query:
        games_list = games_list.filter(title__icontains=search_query)

    if players_count:
        games_list = games_list.filter(min_players=players_count)

    user_id = request.session.get('user_id')
    user = Users.objects.filter(id=user_id).first() if user_id else None
    
    if user:
        user.is_authenticated = True
    else:
        user = type('AnonymousUser', (object,), {'is_authenticated': False})()

    return render(request, 'games/home.html', {
        'games': games_list,
        'user': user,
        'search_query': search_query,
        'players_count': players_count
    })

def game_detail_view(request, game_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.id, g.name, g.rules, g.is_active, g.app_name
            FROM "games" g
            LEFT JOIN "user_favorites" f ON g.id = f.game_id
            WHERE g.id = %s
            GROUP BY g.id, g.name, g.rules, g.is_active, g.app_name
        """, [game_id])
        row = cursor.fetchone()
        
        if not row:
            return redirect('games:home')
        
        game = {
            'id': row[0],
            'name': row[1],   
            'title': row[1], 
            'rules': row[2],
            'is_active': row[3],
            'app_name': row[4]
        }

    is_favorite = False
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM "user_favorites" 
                WHERE "user_id" = %s AND "game_id" = %s
            """, [user_id, game_id])
            if cursor.fetchone():
                is_favorite = True 

    context = {
        'game': game,
        'is_favorite': is_favorite
    }
    return render(request, 'games/game_detail.html', context)

@csrf_exempt
def toggle_favorite(request, game_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    user_id = request.session['user_id']
    current_time = timezone.now()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1 FROM "user_favorites" 
            WHERE "user_id" = %s AND "game_id" = %s
        """, [user_id, game_id])
        exists = cursor.fetchone()

        if exists:
            cursor.execute("""
                DELETE FROM "user_favorites" 
                WHERE "user_id" = %s AND "game_id" = %s
            """, [user_id, game_id])
            status = "removed"
        else:
            cursor.execute("""
                INSERT INTO "user_favorites" ("user_id", "game_id", "added_at") 
                VALUES (%s, %s, %s)
            """, [user_id, game_id, current_time])
            status = "added"

        return JsonResponse({'status': status})

@csrf_exempt
def save_game_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = request.session.get('user_id')
            user_obj = None
            if user_id:
                user_obj = Users.objects.get(id=user_id)

            GameSession.objects.create(
                user=user_obj,  
                game_id=data.get('game_id'),
                score=data.get('score', 0),
                current_step=data.get('steps', 0),
                status='completed'
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error'}, status=400)