from django.utils import timezone
from django.test import TestCase
from django.test import Client
from .models import Game, Player


class TestApplication(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_highscore(self):
        client = Client()
        response = client.get('/highscore')
        self.assertEqual(response.status_code, 200)

    def test_settings(self):
        testplayer1 = Player.objects.create(name="Testplayer1")
        testplayer2 = Player.objects.create(name="Testplayer2")
        Game.objects.create(gamedate=timezone.now(), player_1=testplayer1, player_2=testplayer2, score_1=5, score_2=5)
        client = Client()
        response = client.get('/settings')
        self.assertEqual(response.status_code, 200)

    def test_settings_nogame(self):
        client = Client()
        response = client.get('/settings')
        self.assertEqual(response.status_code, 404)

    def test_newgame(self):
        client = Client()
        response = client.get('/newgame')
        self.assertEqual(response.status_code, 302)

    def test_resetscore(self):
        testplayer1 = Player.objects.create(name="Testplayer1")
        testplayer2 = Player.objects.create(name="Testplayer2")
        Game.objects.create(gamedate=timezone.now(), player_1=testplayer1, player_2=testplayer2, score_1=5, score_2=5)
        client = Client()
        response = client.get('/resetscore')
        self.assertEqual(response.status_code, 302)

    def test_resetscore_nogame(self):
        client = Client()
        response = client.get('/resetscore')
        self.assertEqual(response.status_code, 404)

    def test_ajax_updatescore(self):
        testplayer1 = Player.objects.create(name="Testplayer1")
        testplayer2 = Player.objects.create(name="Testplayer2")
        Game.objects.create(gamedate=timezone.now(), player_1=testplayer1, player_2=testplayer2, score_1=5, score_2=5)
        client = Client()
        response = client.get('/ajax/updatescore')
        self.assertEqual(response.status_code, 200)

    def test_ajax_updatescore_nogame(self):
        client = Client()
        response = client.get('/ajax/updatescore')
        self.assertEqual(response.status_code, 400)

    def test_saveplayer(self):
        testplayer1 = Player.objects.create(name="Testplayer1")
        testplayer2 = Player.objects.create(name="Testplayer2")
        game = Game.objects.create(gamedate=timezone.now(), player_1=testplayer1, player_2=testplayer2, score_1=5, score_2=5)
        client = Client()
        response = client.post('/saveplayer',{'game': game.id, 'player1': testplayer2.id, 'player2': testplayer1.id})
        self.assertEqual(response.status_code, 302)

    def test_saveplayer_nodata(self):
        client = Client()
        response = client.get('/saveplayer')
        self.assertEqual(response.status_code, 302)
