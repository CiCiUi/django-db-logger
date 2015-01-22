# encoding: utf-8
from __future__ import unicode_literals
import logging
from django.contrib.admin import AdminSite
from django.test import TestCase
from django_db_logger.admin import StatusLogAdmin
from .models import StatusLog


class TestDbLogger(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('db_logger')
        self.status_log_admin = StatusLogAdmin(StatusLog, AdminSite())

    def __test_log_aux(self, msg, fn, level):
        fn(msg)
        log_queryset = StatusLog.objects.filter(msg=msg)
        self.assertEqual(log_queryset.count(), 1)
        log = log_queryset.get()
        self.assertEqual(level, log.level)
        self.assertIsNone(log.trace)
        return log

    def test_log(self):
        log = self.__test_log_aux('Info Message - 信息', self.logger.info, logging.INFO)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: green;">Info Message - 信息</span>')

        log = self.__test_log_aux('Debug Message - 调试', self.logger.debug, logging.DEBUG)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: orange;">Debug Message - 调试</span>')

        log = self.__test_log_aux('Warning Message - 警告', self.logger.warning, logging.WARNING)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: orange;">Warning Message - 警告</span>')

        log = self.__test_log_aux('Error Message - 错误', self.logger.error, logging.ERROR)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: red;">Error Message - 错误</span>')

        log = self.__test_log_aux('Fatal Message - 致命错误', self.logger.fatal, logging.FATAL)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: red;">Fatal Message - 致命错误</span>')
        self.assertEqual(self.status_log_admin.traceback(log), '<pre><code></code></pre>')

    def test_exception(self):
        exception_message = 'Exception Message'
        try:
            raise Exception(exception_message)
        except Exception as e:
            self.logger.exception(e)

        log_queryset = StatusLog.objects.filter(msg=exception_message)
        self.assertEqual(log_queryset.count(), 1)
        log = log_queryset.get()
        self.assertEqual(logging.ERROR, log.level)
        self.assertIsNotNone(log.trace)
