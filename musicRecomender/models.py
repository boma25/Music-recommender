from django.db import models

# Create your models here.


class Music(models.Model):
    Title = models.CharField(max_length=200)
    Artist = models.CharField(max_length=200)
    Genre = models.CharField(max_length=200)
    Beats_per_minute = models.IntegerField(default=0)
    Danceability = models.IntegerField(default=0)
    music_id = models.IntegerField(default=0)

    def __str__(self):
        return self.Title
