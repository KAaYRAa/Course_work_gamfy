from django.db import models
from django.utils import timezone

class Games(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, db_column='name') 
    description = models.TextField(blank=True, null=True)
    rules = models.TextField(blank=True, null=True)
    min_players = models.IntegerField(default=1)
    has_timer = models.BooleanField(default=False)
    app_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'games'

    def __str__(self):
        return self.title

class FavoriteGame(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, db_column='user_id')
    game = models.ForeignKey('Games', on_delete=models.CASCADE, db_column='game_id')
    added_at = models.DateTimeField(default=timezone.now, db_column='added_at')

    class Meta:
        managed = False           
        db_table = 'user_favorites' 
        unique_together = ('user', 'game')

class GameSession(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey('Games', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='completed')
    current_step = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'game_session'