from argparse import Namespace
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('posts')
app.config_from_object('django.conf:setting', namespace = 'CELERY')

app.autodiscover_tasks()