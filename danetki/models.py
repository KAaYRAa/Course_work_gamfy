from django.db import models

class GameContent(models.Model):
    game = models.ForeignKey(
        'games.Games', 
        on_delete=models.CASCADE, 
        db_column='game_id', 
        related_name='danetki_contents' 
    )
    content_text = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    extra_info = models.TextField()

    class Meta:
        managed = False
        db_table = 'game_content'