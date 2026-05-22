import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Games

def mafia_rules_view(request):
    game = get_object_or_404(Games, id=3)
    return render(request, 'games/game_detail.html', {'game': game})

def mafia_play_view(request):
    request.session['mafia_roles'] = {}
    request.session['mafia_alive'] = []
    request.session['mafia_eliminated'] = []
    request.session['mafia_current_step'] = 0
    request.session.modified = True
    return render(request, 'mafia/play.html')

@csrf_exempt
def distribute_roles_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            counts = data.get('counts', {})
            
            role_pool = []
            for role, count in counts.items():
                for _ in range(int(count)):
                    role_pool.append(role)

            random.shuffle(role_pool)

            server_roles = {}
            alive_players = []
            for i, role in enumerate(role_pool):
                player_id = str(i + 1)
                server_roles[player_id] = role
                alive_players.append(player_id)

            request.session['mafia_roles'] = server_roles
            request.session['mafia_alive'] = alive_players
            request.session['mafia_eliminated'] = []
            request.session['mafia_current_step'] = 1
            request.session.modified = True

            return JsonResponse({
                'total_players': len(alive_players), 
                'current_step': 1
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_my_role_api(request):
   
    player_id = request.GET.get('player_id')
    server_roles = request.session.get('mafia_roles', {})
    
    if player_id in server_roles:
        return JsonResponse({'role': server_roles[player_id]})
    
    return JsonResponse({'role': None}, status=403)

@csrf_exempt
def eliminate_player_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            target_id = str(data.get('player_id'))
            
            alive_players = request.session.get('mafia_alive', [])
            eliminated_players = request.session.get('mafia_eliminated', [])
            server_roles = request.session.get('mafia_roles', {})

            if target_id != "nobody" and target_id in eliminated_players:
                return JsonResponse({'error': 'Гравець вже вибув!'}, status=400)

            if target_id != "nobody" and target_id in alive_players:
                alive_players.remove(target_id)
                eliminated_players.append(target_id)

            request.session['mafia_current_step'] = request.session.get('mafia_current_step', 1) + 1
            request.session['mafia_alive'] = alive_players
            request.session['mafia_eliminated'] = eliminated_players
            request.session.modified = True

            alive_roles = [server_roles[pid] for pid in alive_players]
            mafia_count = alive_roles.count('Мафія')
            citizens_count = len(alive_roles) - mafia_count

            game_over = False
            winner = None
            if mafia_count == 0:
                game_over = True
                winner = "Мирні"
            elif mafia_count >= citizens_count:
                game_over = True
                winner = "Мафія"

            active_list = [{'id': pid, 'name': f"Гравець {pid}"} for pid in alive_players]
            final_distribution = server_roles if game_over else {}

            return JsonResponse({
                'alive_players': active_list,
                'current_step': request.session['mafia_current_step'],
                'game_over': game_over,
                'winner': winner,
                'final_distribution': final_distribution
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)