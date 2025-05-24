from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Clean users table'

    def handle(self, *args, **kwargs):
        count = User.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No users to delete.'))
            return

        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{count} users deleted.'))
