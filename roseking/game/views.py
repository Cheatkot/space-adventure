from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BrezelWar


@login_required
def game_demo(request):
    return render(request, "game/game-demo.html", {"range": range(9), "game_id": "test123456789"})


@login_required
def main_game(request, game_id):
    return render(request, "game/main-game.html", {"range": range(9), "game_id": game_id})


@login_required
def game_history(request):
    ls = BrezelWar.objects.filter(player_one_username__exact=request.user.username)
    if not ls.exists():
        ls = BrezelWar.objects.filter(player_two_username__exact=request.user.username)

    return render(request, "game/game-history.html", {"ls": ls})
