from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def game_demo(request):
    return render(request, "game/game-demo.html", {"range": range(9), "game_id": "test123456789"})


@login_required
def main_game(request, game_id):
    return render(request, "game/main-game.html", {"range": range(9), "game_id": game_id})
