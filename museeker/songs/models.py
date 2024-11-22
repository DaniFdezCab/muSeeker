from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    discography = models.CharField(max_length=100)
    duration = models.FloatField()
    spotify_link = models.CharField(max_length=250)    
    

    def __str__(self):
        return self.title