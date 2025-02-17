# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-game/", views.new_game, name="new_game"),
    path("make-move/", views.make_move, name="make_move"),
]
