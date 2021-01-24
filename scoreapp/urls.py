from django.urls import path

from . import views

app_name = 'scoreapp' # define namespace for app
urlpatterns = [
    path('', views.index, name='index'),                                # Mainpage
    path('resetscore', views.resetscore, name='resetscore'),            # Form handler to reset score
    path('newgame', views.newgame, name='newgame'),                     # create new game
    path('settings', views.settings, name='settings'),                  # Settings page
    path('saveplayer', views.saveplayer, name='saveplayer'),            # Form handler to save players
    path('highscore', views.highscore, name='highscore'),               # Highscore page
    path('controller', views.controller, name='controller'),            # Controller page
    path('ajax/updatescore', views.updatescore, name='updatescore'),    # Ajax Update Score
    path('ajax/scorechange', views.scorechange, name='scorechange'),    # Change score via Ajax
]
