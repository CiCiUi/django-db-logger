from __future__ import unicode_literals
import logging

from django.contrib import admin
from django.utils.html import format_html

from .models import StatusLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('colored_msg', 'traceback', 'create_datetime_format')
    list_display_links = ('colored_msg', )
    list_filter = ('level', )
    list_per_page = 10

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
        return instance.create_datetime.strftime('%Y-%m-%d %X')
    create_datetime_format.short_description = 'Create Datetime'


admin.site.register(StatusLog, StatusLogAdmin)