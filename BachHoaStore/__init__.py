from __future__ import absolute_import, unicode_literals

# Cài đặt Celery khi khởi động Django
from .celery import app as celery_app

__all__ = ['celery_app']
