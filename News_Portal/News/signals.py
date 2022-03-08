from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.header} {instance.time.strftime("%d %m %Y")}'
    else:
        subject = f'Post changed: {instance.header} {instance.time.strftime("%d %m %Y")}'
    for cat in instance.category.all():
        for sub in cat.subscribers.all():
            if created:
                html_content = render_to_string('post_created.html', {'sub': sub, })
            else:
                html_content = render_to_string('post_changed.html', {'sub': sub, })
            msg = EmailMultiAlternatives(
                subject=subject,
                body=instance.text,
                from_email='elistratishka@yandex.ru',
                to=[sub.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
