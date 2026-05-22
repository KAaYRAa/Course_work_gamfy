import random
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

def play_view(request):

    return render(request, 'puzzle/play.html')

def get_puzzle_data(request):

    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT "id", "content_text" 
                FROM "game_content" 
                WHERE "game_id" = 5 
                ORDER BY RANDOM() LIMIT 1
            """)
            row = cursor.fetchone()
            
            if not row:
                return JsonResponse({'error': 'Слів не знайдено'}, status=404)
            
            content_id, secret_word = row
            
            cursor.execute("""
                SELECT "detail_text" 
                FROM "game_details" 
                WHERE "content_id" = %s 
                ORDER BY "order_index" ASC
            """, [content_id])
            
            hints = [r[0] for r in cursor.fetchall()]
            
            if not hints:
                return JsonResponse({'error': f'Немає підказок для "{secret_word}"'}, status=404)

            matrix_size = 3
            puzzle_matrix = []
            hint_index = 0
            
            for r in range(matrix_size):
                row_data = []
                for c in range(matrix_size):
                    if hint_index < len(hints):
                        text = hints[hint_index]
                    else:
                        text = "Додаткова підказка відсутня"
                    
                    row_data.append({
                        'row': r,
                        'col': c,
                        'text': text,
                        'is_revealed': False
                    })
                    hint_index += 1
                puzzle_matrix.append(row_data)

            return JsonResponse({
                'secret_word': secret_word,
                'puzzle_matrix': puzzle_matrix,
                'matrix_size': matrix_size
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def check_puzzle_guess_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_guess = data.get('guess', '').lower().strip()
            secret_word = data.get('secret_word', '').lower().strip()
            
            is_correct = True
            if len(user_guess) != len(secret_word):
                is_correct = False
            else:
                for i in range(len(secret_word)):
                    if user_guess[i] != secret_word[i]:
                        is_correct = False
                        break
            
            return JsonResponse({'is_correct': is_correct})
        except Exception as e:

            print(f"Критична помилка валідації пазлу: {e}")
            return JsonResponse({'error': str(e)}, status=400)