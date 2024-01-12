from django.shortcuts import render, get_object_or_404
from .models import Song
from .chordpro import ChordPro

def songs(request):
    songs = Song.objects.all()
    context = {
        "songs": songs
    }
    return render(request, "songs.html", context)


def render_song(request, pk):
    transpose = request.GET.get("transpose")
    bass_only = "bass_only" in request.GET
    transpose = int(transpose) if transpose is not None else 0

    song = get_object_or_404(Song, pk=pk)
    context = {
        "song_lines": ChordPro.render_chordpro(song.chordpro, transpose, song.key, bass_only),
        "song_title": song.title
    }
    return render(request, "song.html", context)

def view_chord(request, chord):
    context = {
        "chord_name": chord,
        "notes": ChordPro.get_chord_data(chord),
    }

    return render(request, "chord.html", context)