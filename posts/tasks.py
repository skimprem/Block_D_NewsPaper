from celery import shared_task
import time
from .models import Post, PostCategory, Category
from accounts.models import UsersSubscriptions, SubscribeMail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta

# @shared_task
# def hello():
#     time.sleep(10)
#     print("hello, world")

# def send_mails():
#     print('hello from background tasks')

@shared_task
def send_notification(oid):
    post = Post.objects.get(pk=oid)
    post_categories = PostCategory.objects.filter(post=post)
    for post_category in post_categories:
        subscriptions = UsersSubscriptions.objects.filter(category=post_category.category)
        for subscription in subscriptions:
            mail = SubscribeMail(
                username = subscription.user.username,
                title = post.title,
                text =  post.text,
                first_name = subscription.user.first_name,
                last_name = subscription.user.last_name,
                link = post.get_absolute_url()
            )
            mail.save()

            html_content = render_to_string(
                'subscribe_create.html',
                {'mail': mail}
            )

            msg = EmailMultiAlternatives(
                subject=f'{mail.title}',
                body=f'{mail.text}',
                from_email='romanags@yandex.ru',
                to=[subscription.user.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def week_notification():
    initial_date = datetime.today() - timedelta(days=7)
    for category in Category.objects.all():
        posts = Post.objects.filter(pub_time__gt=initial_date.isoformat(), categories=category)
        subscriptions = UsersSubscriptions.objects.filter(category=category)
        for subscription in subscriptions:
            html_content = render_to_string(
                'subscribe_list_create.html',
                {'posts': posts, 'subscription': subscription}
            )
            text_body = ""
            for post in posts:
                text_body = text_body+f'{post.title} \n http://127.0.0.1:8000{post.get_absolute_url()} \n \n'
            msg = EmailMultiAlternatives(
                subject='Рассылка по подписке за неделю',
                body=text_body,
                from_email='romanags@yandex.ru',
                to=[subscription.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()