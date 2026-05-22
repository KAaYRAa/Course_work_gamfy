from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, db_column='avatar_url')

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username