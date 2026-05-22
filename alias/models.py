from django.db import models

class AliasWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, db_column='content_text')
    game_id = models.IntegerField(db_column='game_id')

    class Meta:
        managed = False
        db_table = 'game_content' 

    def __str__(self):
        return self.word

