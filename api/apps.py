from django.apps import AppConfig
# from views import handle_termination

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"


    # def ready(self):
    #     signal.signal(signal.SIGTERM, handle_termination)