from celery import shared_task
from News.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import time


@shared_task
def weekly_message():
    timer = time.strftime('%Y-%m-', time.localtime())
    day = time.strftime('%d', time.localtime())
    for post in Post.objects.filter(time__range=[timer + str(int(day) - 7), timer + day]).distinct():
        for cat in post.category.all():
            posts = Post.objects.filter(time__range=[timer + str(int(day) - 7), timer + day], category=cat).distinct()
            for sub in cat.subscribers.all():
                html_content = render_to_string('post_weekly.html', {'sub': sub, 'posts': posts})
                msg = EmailMultiAlternatives(
                    subject=f'{sub.username}, новости прошедшей недели из Ваших любимых категорий.',
                    body=post.text,
                    from_email='elistratishka@yandex.ru',
                    to=[sub.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


@shared_task
def post_message():
    pass
