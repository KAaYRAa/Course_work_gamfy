import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import GameContent, DilemmaVote
from django.db.models import Count, Q, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
import json 
from django.views.decorators.csrf import csrf_exempt

def play_view(request):
    """Відображення ігрового поля гри Дилема"""
    return render(request, 'dilemma/play.html')

def get_dilemmas(request):

    try:
        rows = list(GameContent.objects.filter(game_id=9).values('id', 'content_text'))
        return JsonResponse({'dilemmas': rows})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def vote_dilemma_api(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dilemma_id = data.get('dilemma_id')
            user_choice = data.get('is_agreed', False)

            try:
                dilemma_obj = GameContent.objects.get(id=dilemma_id)
            except GameContent.DoesNotExist:
                return JsonResponse({'error': 'Dilemma not found'}, status=404)

            DilemmaVote.objects.create(
                dilemma=dilemma_obj,
                is_agreed=user_choice
            )

            stats = DilemmaVote.objects.filter(dilemma_id=dilemma_id).aggregate(
                total=Count('id'),
                agreed=Count('id', filter=Q(is_agreed=True))
            )

            total_votes = stats['total'] or 0
            agreed_votes = stats['agreed'] or 0

    
            if total_votes > 0:
                global_agreed_percent = round((agreed_votes / total_votes) * 100)
            else:
                global_agreed_percent = 50 

            global_disagreed_percent = 100 - global_agreed_percent

            return JsonResponse({
                'global_agreed_percent': global_agreed_percent,
                'global_disagreed_percent': global_disagreed_percent,
                'total_community_votes': total_votes
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def vote_dilemma_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dilemma_id = data.get('dilemma_id')
            user_choice = data.get('is_agreed', False) 

            try:
                dilemma_obj = GameContent.objects.get(id=dilemma_id)
            except GameContent.DoesNotExist:
                return JsonResponse({'error': 'Dilemma not found'}, status=404)

            DilemmaVote.objects.create(
                dilemma=dilemma_obj,
                is_agreed=user_choice
            )
            stats = DilemmaVote.objects.filter(dilemma_id=dilemma_id).aggregate(
                total=Count('id'),
                agreed=Count('id', filter=Q(is_agreed=True))
            )

            total_votes = stats['total'] or 0
            agreed_votes = stats['agreed'] or 0

            if total_votes > 0:
                global_agreed_percent = round((agreed_votes / total_votes) * 100)
            else:
                global_agreed_percent = 50 

            global_disagreed_percent = 100 - global_agreed_percent

            return JsonResponse({
                'global_agreed_percent': global_agreed_percent,
                'global_disagreed_percent': global_disagreed_percent,
                'total_community_votes': total_votes
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)