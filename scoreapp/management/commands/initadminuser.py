from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser('admin', 'admin@scoreboard.local', '123')
            print("created new superuser")
        else:
            print("Admin account already exists")
