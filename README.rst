================
django-db-logger
================

I finally switched back to the original app https://github.com/CiCiUi/django-db-logger,
customizing StatusLogAdmin in the local Django project as follows:

```
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django_db_logger.models import StatusLog
from django_db_logger.admin import StatusLogAdmin

################################################################################
# Improved StatusLogAdmin

class StatusLogAdminEx(StatusLogAdmin):
    list_display = ('create_datetime_format', 'colored_msg', 'traceback', )
    list_display_links = ('create_datetime_format', )
    list_filter = ('create_datetime', 'level', )
    readonly_fields = ['logger_name', 'level', 'msg', 'trace', ]
    date_hierarchy = 'create_datetime'

    def create_datetime_format(self, instance):
        return format_html(
            '<span style="white-space: nowrap;">%s</span>' % \
                timezone.localtime(instance.create_datetime).strftime('%Y-%m-%d %X')
        )
    create_datetime_format.short_description = 'Created at'

    def has_add_permission(self, request):
        # Hide "Add" button from admin
        return False

    def has_change_permission(self, request, obj=None):
        # Hide "Save" button from admin
        return False

admin.site.unregister(StatusLog)
admin.site.register(StatusLog, StatusLogAdminEx)
```
