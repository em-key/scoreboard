from django.contrib import admin

# Register your models here.

from .models import Game, Player

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'gamedate', 'player_1','score_1','player_2','score_2')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mail')

admin.site.register(Player,PlayerAdmin)
admin.site.register(Game,GameAdmin)
