from django.urls import path

from . import views

urlpatterns = [
    path("songs/<int:pk>/", views.render_song, name='song'),
    path("songs/", views.songs, name='songs'),
    path("chords/<chord>/", views.view_chord, name='chord'),
]
