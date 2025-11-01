from django.apps import AppConfig



class CommonDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common_data'

    def ready(self):
        import common_data.signals

