from django.apps import AppConfig


class CommonDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common_data'

    def ready(self):
        import common_data.signals

    def create_groups(self, **kwargs):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Student')
        Group.objects.get_or_create(name='Teacher')