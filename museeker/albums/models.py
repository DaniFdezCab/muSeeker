from django.db import models
from django.contrib.auth.models import User

class UserAlbumInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_id = models.IntegerField(null=False)
    rating = models.IntegerField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'album_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.album_id}" if self.is_favorite else f"{self.user.username} - {self.album_id} - {self.rating}"