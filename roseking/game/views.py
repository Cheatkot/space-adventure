from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def game_demo(request):
    return render(request, "game/game-demo.html", {"range": range(9), "game_id": "test123456789"})
