from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        # Register signal handlers (auto-create a Profile for every new user).
        import account.signals  # noqa: F401
