from __future__ import unicode_literals
import logging

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from django_db_logger.config import DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
from .models import StatusLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('create_datetime_format', 'colored_msg', 'traceback', )
    list_display_links = ('colored_msg', )
    list_filter = ('level', )
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
    readonly_fields = ['logger_name', 'level', 'msg', 'trace', ]

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)
    colored_msg.short_description = 'Message'

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return format_html(
            '<span style="white-space: nowrap;">%s</span>' % \
                timezone.localtime(instance.create_datetime).strftime('%Y-%m-%d %X')
        )
    create_datetime_format.short_description = 'Created at'

    def has_add_permission(self, request):
        # Hide "Add" button from admin
        return False


admin.site.register(StatusLog, StatusLogAdmin)
