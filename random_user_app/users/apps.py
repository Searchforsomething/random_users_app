import sys
import threading

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        def run_load_users():
            from django.core.management import call_command
            try:
                call_command('load_random_users')
            except Exception as e:
                print(f'Error loading users: {e}')

        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            threading.Thread(target=run_load_users).start()
