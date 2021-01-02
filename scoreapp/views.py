from operator import itemgetter     # Required to sort dict for highscore
from django.urls import reverse     # needed for handling of django forms
from django.utils import timezone   # used to get current time for new games
from django.http import Http404, HttpResponseRedirect, JsonResponse     # Import for 404 Error page if no game can be selected, Redirect for HTTP form handling and Ajax Json response
from django.db.models import F      # import that Comparison in SQL Query is possible
from django.shortcuts import render, get_object_or_404 # Shortcut function to render template and handing of 404 if HTTP form fails
from .models import Game, Player    # Import of Models - Database Schema


# Ajax

def updatescore(request):
    try:
        activegame = Game.objects.latest('id')
        score1 = activegame.score_1
        score2 = activegame.score_2
        if request.is_ajax and request.method == "GET":
            return JsonResponse({"score1":score1,"score2":score2}, status = 200)
        else:
            return JsonResponse({}, status = 400)
    except Game.DoesNotExist:
        return JsonResponse({}, status = 400)

# Main Page - showing score and give navigation options

def index(request):
    try:
        activegame = Game.objects.latest('id')    # Get active/latest game
    except Game.DoesNotExist:
        newgame(request)
        activegame = Game.objects.latest('id')
    context = {
            'active_game': activegame,
        }
    return render(request, 'scoreapp/index.html',context)

def resetscore(request):
    try:
        game = Game.objects.latest('id')
        game.score_1 = 0
        game.score_2 = 0
        game.save()
    except Game.DoesNotExist as error:
        raise Http404("Error - could not resolve game") from error
    return HttpResponseRedirect(reverse('scoreapp:index'))

def newgame(request):
    try:
        lastgame = Game.objects.latest('id')    # Get active/latest game
        Game.objects.create(gamedate=timezone.now(), player_1=lastgame.player_1, player_2=lastgame.player_2, score_1=0, score_2=0)
    except Game.DoesNotExist:
        try:
            player1 = Player.objects.get(name='Spieler-1')
        except Player.DoesNotExist:
            player1 = Player.objects.create(name="Spieler-1")
        try:
            player2 = Player.objects.get(name='Spieler-2')
        except Player.DoesNotExist:
            player2 = Player.objects.create(name="Spieler-2")
        Game.objects.create(gamedate=timezone.now(), player_1=player1, player_2=player2, score_1=0, score_2=0)
    return HttpResponseRedirect(reverse('scoreapp:index'))

# Settings page - change players (in future add and remove players)

def settings(request):
    try:
        activegame = Game.objects.latest('id')
        player_list = Player.objects.all()
        context = {
            'active_game': activegame,
            'player_list': player_list
        }
    except Game.DoesNotExist as error:
        raise Http404("Error - could not resolve game") from error
    return render(request, 'scoreapp/settings.html',context)

def saveplayer(request):
    if request.method == 'POST':
        game = get_object_or_404(Game, pk=request.POST['game'])
        player1 = get_object_or_404(Player, pk=request.POST['player1'])
        player2 = get_object_or_404(Player, pk=request.POST['player2'])
        game.player_1 = player1
        game.player_2 = player2
        game.save()

    return HttpResponseRedirect(reverse('scoreapp:index'))

# Highscore page

def highscore(request):
    player_all = Player.objects.all().exclude(name='Spieler-1').exclude(name='Spieler-2')
    highscore_list = []

    for player in player_all:
        wins = (Game.objects.filter(score_1__gt=F('score_2')).filter(player_1__id=player.id) | Game.objects.filter(score_2__gt=F('score_1')).filter(player_2__id=player.id)).count()
        highscore_list.append({'player':player.name, 'wins':wins})
    highscore_list = sorted(highscore_list, key=itemgetter('wins'), reverse=True)
    context = {
        'highscore_list': highscore_list
    }
    return render(request, 'scoreapp/highscore.html',context)
