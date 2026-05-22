from django.db import models

class GameContent(models.Model):
    game = models.ForeignKey('games.Games', on_delete=models.CASCADE, db_column='game_id')
    content_text = models.CharField(max_length=255)

    class Meta:
        managed = False  
        db_table = 'game_content'

class GameDetails(models.Model):
    content = models.ForeignKey(GameContent, on_delete=models.CASCADE, db_column='content_id')
    detail_text = models.TextField()
    order_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game_details'