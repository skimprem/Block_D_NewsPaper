# from django.core.mail import send_mail
from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(10)
    print("hello, world")

# def send_mails():
#     print('hello from background tasks')