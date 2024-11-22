from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=100)
    artists = models.CharField(max_length=100)
    date = models.DateField(default=None)
    calification = models.FloatField()
    cover = models.ImageField(upload_to='albums/covers/')
    spotify_link = models.CharField(max_length=250)
    awards = models.CharField(max_length=100)
    


    def __str__(self):
        return self.title