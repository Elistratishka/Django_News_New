import logging
import time

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from News.models import Post

logger = logging.getLogger(__name__)


# def my_job():
#     timer = time.strftime('%Y-%m-', time.localtime())
#     day = time.strftime('%d', time.localtime())
#     for post in Post.objects.filter(time__range=[timer + str(int(day) - 7), timer + day]).distinct():
#         for cat in post.category.all():
#             posts = Post.objects.filter(time__range=[timer + str(int(day) - 7), timer + day], category=cat).distinct()
#             for sub in cat.subscribers.all():
#                 html_content = render_to_string('post_weekly.html', {'sub': sub, 'posts': posts})
#                 msg = EmailMultiAlternatives(
#                     subject=f'{sub.username}, новости прошедшей недели из Ваших любимых категорий.',
#                     body=post.text,
#                     from_email='elistratishka@yandex.ru',
#                     to=[sub.email],
#                 )
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(my_job, trigger=CronTrigger(second="*/10"), id="my_job", max_instances=1, replace_existing=True)
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
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
