import logging

from django.contrib import admin
from django.utils.html import format_html

from .models import StatusLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('colored_msg', 'traceback', 'create_datetime')
    list_display_links = ('colored_msg', )
    list_filter = ('level', )
    list_per_page = 10

    @staticmethod
    def colored_msg(instance):
        if instance.level in [logging.NOTSET, logging.INFO, logging]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    @staticmethod
    def traceback(instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace)


admin.site.register(StatusLog, StatusLogAdmin)