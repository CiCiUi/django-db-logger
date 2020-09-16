import logging

from django_db_logger.config import DJANGO_DB_LOGGER_ENABLE_FORMATTER, MSG_STYLE_SIMPLE
from django_db_logger.config import DJANGO_DB_LOGGER_MAX_LOG_RECORDS


db_default_formatter = logging.Formatter()


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import StatusLog

        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace
        }

        StatusLog.objects.create(**kwargs)
        self.cleanup_status_log()

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)

    def cleanup_status_log(self):
        from .models import StatusLog
        if DJANGO_DB_LOGGER_MAX_LOG_RECORDS > 0 and \
           StatusLog.objects.count() >DJANGO_DB_LOGGER_MAX_LOG_RECORDS:
                # Remove olders records
                queryset = StatusLog.objects.all()[DJANGO_DB_LOGGER_MAX_LOG_RECORDS:]
                for row in queryset.iterator():
                    row.delete()
