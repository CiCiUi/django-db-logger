import logging
import traceback

from .models import StatusLog


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        trace = None

        if record.exc_info:
            trace = traceback.format_exc()

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': record.getMessage(),
            'trace': trace
        }

        StatusLog.objects.create(**kwargs)