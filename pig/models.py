from django.db import models

class GameContent(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey('games.Games', on_delete=models.CASCADE, db_column='game_id', related_name='pig_contents')
    content_text = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'game_content'

    def __str__(self):
        return self.content_text