# Generated by Django 4.0 on 2022-02-17 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News', '0002_alter_subscribe_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subs', through='News.Subscribe', to=settings.AUTH_USER_MODEL),
        ),
    ]