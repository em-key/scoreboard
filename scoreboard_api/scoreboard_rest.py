import os
import sys
import connexion
import django
from connexion.exceptions import OAuthProblem, ProblemException


# append path that module can be found
sys.path.append('../')

# the django setup needs access to the settings file
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "scoreboard.settings_dev")
django.setup ()

from scoreapp.models import Game

# from scoreboard import settings
# from django.core.management import setup_environ
# setup_environ(settings)


TOKEN_DB = {
    '1234': {
        'uid': 1
    }
}

def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)
    if not info:
        raise OAuthProblem('Invalid token')
    return info


def post_change_players_score(player: bool, points: int) -> str:
    try:
        game = Game.objects.latest('id')
        if player:
            game.score_1 = game.score_1 + points
        else:
            game.score_2 = game.score_2 + points
        game.save()
    except Game.DoesNotExist as error:
        raise ProblemException(
            title='Error - could not resolve game',
            status=404
        ) from error
    return "success"

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='./')
    app.add_api('scoreboard_rest.openapi.yml', arguments={'title': 'Scoreboard Swagger API'})
    app.run()
