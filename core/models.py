from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=80)
    original_title = models.CharField(max_length=80, blank=True, null=True)
    key = models.CharField(max_length=4)
    chordpro = models.TextField()
    time_signature = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title
    

class SongbookEntry(models.Model):
    songbook = models.ForeignKey("Songbook", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.songbook} {self.number}. {self.song}"

class Songbook(models.Model):
    name = models.CharField(max_length=80)
    songs = models.ManyToManyField(to=Song, through=SongbookEntry)

    def __str__(self):
        return self.name