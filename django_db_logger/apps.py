from django.apps import AppConfig


class DbLoggerAppConfig(AppConfig):
    name = 'django_db_logger'
    verbose_name = 'Db logging'
    # Explicitly set default auto field type to avoid migrations in Django 3.2+
    default_auto_field = 'django.db.models.AutoField'
