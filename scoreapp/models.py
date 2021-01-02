from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Game(models.Model):
    gamedate = models.DateTimeField('gamedate')
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE,related_name='player_1')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE,related_name='player_2')
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)

    def __str__(self):
        # return str(self.id), str(self.gamedate)
        return "Game " + "{0:0=3d}".format(self.id) + " (" + str(self.gamedate) + ")"
