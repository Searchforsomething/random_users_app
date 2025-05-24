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
                print(f'Ошибка при загрузке пользователей: {e}')

        threading.Thread(target=run_load_users).start()
