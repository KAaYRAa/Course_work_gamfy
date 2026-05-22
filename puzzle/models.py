from django.db import models

class GameDetail(models.Model):
    content_id = models.IntegerField() 
    detail_text = models.TextField()  
    order_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game_detail' 