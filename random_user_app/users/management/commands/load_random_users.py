import requests
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Load 1000 unique random users from API'

    def handle(self, *args, **kwargs):
        if User.objects.exists():
            self.stdout.write(self.style.WARNING("Users already exist. Skipping."))
            return

        TARGET_COUNT = 1000
        created_count = 0
        seen_emails = set(User.objects.values_list("email", flat=True))
        users_to_create = []

        while created_count < TARGET_COUNT:
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

                if len(new_users) + created_count >= TARGET_COUNT:
                    break

            User.objects.bulk_create(new_users)
            created_count += len(new_users)
            self.stdout.write(f"Created {created_count} users...")

        self.stdout.write(self.style.SUCCESS(f"{created_count} unique users created."))
