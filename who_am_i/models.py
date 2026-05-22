from django.db import models

class GameContent(models.Model):
    game = models.ForeignKey('games.Games', on_delete=models.CASCADE, db_column='game_id', related_name='whoami_contents')
    content_text = models.CharField(max_length=255) 

    class Meta:
        managed = False
        db_table = 'game_content'