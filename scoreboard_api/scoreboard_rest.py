import os
import sys
import connexion
import django
from connexion.exceptions import OAuthProblem, ProblemException


# append path that module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# the django setup needs access to the settings file
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "scoreboard.settings_prod")
django.setup ()

from scoreapp.models import Game

# from scoreboard import settings
# from django.core.management import setup_environ
# setup_environ(settings)


TOKEN_DB = {
    os.environ.get("API_KEY"): {
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

# Setup Flask App
scoreboard_rest = connexion.FlaskApp(__name__, specification_dir='./')
scoreboard_rest.add_api('scoreboard_openapi.yml')

# Setup application callable for WSGI
application = scoreboard_rest.app

# to run in devellopement where script is called directly
if __name__ == '__main__':
    scoreboard_rest.run(port=8080)
