from django.apps import AppConfig


class ProfileAppConfig(AppConfig):
    name = 'ProfileApp'

    def ready(self):
        import ProfileApp.signals
