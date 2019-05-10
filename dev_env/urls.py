from django.contrib import admin
from django.urls import path

from django_db_logger.views import __gen_500_errors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__gen_500/', __gen_500_errors)
]
