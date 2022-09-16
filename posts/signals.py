import re
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import Post, PostCategory, Category
from accounts.models import UsersSubscriptions, SubscribeMail
from django.template.loader import render_to_string

@receiver(m2m_changed, sender=PostCategory)
def subscribe_notify(sender, instance, **kwargs):
    post = instance
    post_title = post.title
    post_text = post.text
    post_categories = PostCategory.objects.filter(post=post)
    for post_category in post_categories:
        subscriptions = UsersSubscriptions.objects.filter(category=post_category.category)
        print(subscriptions)
        for subscription in subscriptions:
            print(subscription)
            mail = SubscribeMail(
                username = subscription.user.username,
                title = post_title,
                text =  post_text,
                first_name = subscription.user.first_name,
                last_name = subscription.user.last_name,
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
    # send_mail(
    #     subject=post_title,
    #     message=post_title,
    #     from_email='romanags@yandex.ru',
    #     recipient_list=['roman.ags@gmail.com']
    # )