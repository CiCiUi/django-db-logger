================
django-db-logger
================

Django logging in database


Quick start
-----------

1. Install::

    pip install django-db-logger

2. Add "django_db_logger" to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
        ...
        'django_db_logger',
    )

3. Add handler and logger to `LOGGING` setting like this::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s %(message)s'
            },
        },
        'handlers': {
            'db_log': {
                'level': 'DEBUG',
                'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
            },
        },
        'loggers': {
            'db': {
                'handlers': ['db_log'],
                'level': 'DEBUG'
            }
        }
    }

4. Run `python manage.py migrate` to create django-db-logger models.
5. Use `django-db-logger` like this::

    import logging
    db_logger = logging.getLogger('db')

    db_logger.info('info message')
    db_logger.warning('warning message')

    try:
        1/0
    except Exception as e:
        db_logger.exception(e)

