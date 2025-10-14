# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):  # <-- Este es el nombre que necesitamos
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'