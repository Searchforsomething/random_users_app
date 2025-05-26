from email.policy import default

import requests
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Load unique random users from API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1000,
            help='Number of unique users to load (default: 1000)'
        )
        parser.add_argument(
            '--init',
            type=bool,
            default=False,
            help='Used for marking initial users adding'
        )

    def handle(self, *args, **kwargs):
        if kwargs['init'] and User.objects.exists():
            self.stdout.write(self.style.WARNING("Users already exist. Skipping."))
            return

        target_count = kwargs['count']
        created_count = 0
        seen_emails = set(User.objects.values_list("email", flat=True))
        users_to_create = []

        while created_count < target_count:
            response = requests.get("https://randomuser.me/api/?results=100")
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR("Failed to fetch users from API"))
                return

            users_data = response.json().get("results", [])
            new_users = []

            for item in users_data:
                email = item['email']
                if email in seen_emails:
                    continue

                seen_emails.add(email)
                location = f"{item['location']['city']}, {item['location']['country']}"
                new_users.append(User(
                    gender=item['gender'],
                    first_name=item['name']['first'],
                    last_name=item['name']['last'],
                    phone=item['phone'],
                    email=email,
                    location=location,
                    thumbnail=item['picture']['thumbnail'],
                ))

                if len(new_users) + created_count >= target_count:
                    break

            User.objects.bulk_create(new_users)
            created_count += len(new_users)
            self.stdout.write(f"Created {created_count} users...")

        self.stdout.write(self.style.SUCCESS(f"{created_count} unique users created."))
