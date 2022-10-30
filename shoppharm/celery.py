"""Celery.py"""
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppharm.settings')
app = Celery('shoppharm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
