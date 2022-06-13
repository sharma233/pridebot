from django.core.management.base import BaseCommand, CommandError
from twitterbot.utils import scrape_profile_pics


class Command(BaseCommand):
    help = "Scrapes Twitter user profile pics and stores them"

    def handle(self, *args, **options):
        scrape_profile_pics()

        self.stdout.write(self.style.SUCCESS("Successfuly scraped profile pics"))
