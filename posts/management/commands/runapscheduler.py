import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from posts.models import Post, PostCategory, Category
from accounts.models import UsersSubscriptions, SubscribeMail
from django.template.loader import render_to_string
import datetime
 
 
logger = logging.getLogger(__name__)
 
 
def week_subscribe():
    initial_date = datetime.datetime.today() - datetime.timedelta(days=7)
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

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            week_subscribe,
            trigger=CronTrigger(day="*/7"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="week_subscribe",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'week_subscribe'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")