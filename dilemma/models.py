from django.db import models
from crocodile.models import GameContent


class GameContent(models.Model):
    game = models.ForeignKey('games.Games', on_delete=models.CASCADE, db_column='game_id', related_name='dilemma_contents')
    content_text = models.CharField(max_length=255)
        
    class Meta:
        managed = False
        db_table = 'game_content'

class DilemmaVote(models.Model):
    dilemma = models.ForeignKey(
        GameContent, 
        on_delete=models.CASCADE, 
        db_column='dilemma_id',
        related_name='votes'
    )
    is_agreed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dilemma_votes'