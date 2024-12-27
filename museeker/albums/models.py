from django.db import models
from django.contrib.auth.models import User

class UserAlbumInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'album_title']
    
    def __str__(self):
        return f"{self.user.username} - {self.album_title}" if self.is_favorite else f"{self.user.username} - {self.album_title} - {self.rating}"