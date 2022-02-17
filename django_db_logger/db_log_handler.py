import logging

from django_db_logger.config import DJANGO_DB_LOGGER_ENABLE_FORMATTER, DJANGO_DB_LOGGER_REQUEST_DETAILS, \
    DJANGO_DB_LOGGER_REQUEST_DETAILS_PATH, DJANGO_DB_LOGGER_REQUEST_DETAILS_METHOD, \
    DJANGO_DB_LOGGER_REQUEST_DETAILS_GET_PARAMS, DJANGO_DB_LOGGER_REQUEST_DETAILS_POST_PARAMS

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

        if getattr(record, 'request', None) and DJANGO_DB_LOGGER_REQUEST_DETAILS:
            kwargs['details'] = {}
            if DJANGO_DB_LOGGER_REQUEST_DETAILS_PATH:
                kwargs['details']['path'] = getattr(record.request, 'path', None)

            if DJANGO_DB_LOGGER_REQUEST_DETAILS_METHOD:
                kwargs['details']['method'] = getattr(record.request, 'method', None)

            if DJANGO_DB_LOGGER_REQUEST_DETAILS_GET_PARAMS:
                kwargs['details']['get_params'] = getattr(record.request, 'GET', None)

            if DJANGO_DB_LOGGER_REQUEST_DETAILS_POST_PARAMS:
                kwargs['details']['post_params'] = getattr(record.request, 'POST', None)

        StatusLog.objects.create(**kwargs)

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
