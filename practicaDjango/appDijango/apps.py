from django.apps import AppConfig


class AppdijangoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appDijango"

    def ready(self):
        import appDijango.signals  # Asegúrate de que el nombre sea correcto, puede ser appDjango o algo más