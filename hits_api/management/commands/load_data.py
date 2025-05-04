# Standard Library Imports
import random

# Third-party Imports
from faker import Faker
from django.core.management.base import BaseCommand

# Local Imports
from hits_api.models import Hit, Artist


class Command(BaseCommand):
    help = "Load initial data into the database"

    def handle(self, *args, **kwargs):
        fake = Faker()
        artists = []
        for _ in range(3):
            artist = Artist.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name()
            )
            artists.append(artist)

        for _ in range(20):
            title = fake.sentence(nb_words=3).rstrip(".")
            Hit.objects.create(title=title, artist=random.choice(artists))

        self.stdout.write(self.style.SUCCESS("Successfully loaded data"))
