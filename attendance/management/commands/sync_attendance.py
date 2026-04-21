from django.core.management.base import BaseCommand
from attendance.sync import sync_from_device 


class Command(BaseCommand):
    help = 'Fetches data from the biometric device'

    def handle(self, *args, **options):
        sync_from_device()
        self.stdout.write("Sync successful!")