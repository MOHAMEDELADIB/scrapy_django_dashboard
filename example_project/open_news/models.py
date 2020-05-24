from __future__ import unicode_literals  # Stage 2 Update (Python 3)
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from scrapy_djangoitem import DjangoItem
from scrapy_django_dashboard.models import Scraper, SchedulerRuntime
# https://stackoverflow.com/a/60720922
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(
        Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(
        SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=200)
    # https://stackoverflow.com/a/44026807
    news_website = models.ForeignKey(
        NewsWebsite, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    thumbnail = models.CharField(max_length=200, blank=True)
    checker_runtime = models.ForeignKey(
        SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class ArticleItem(DjangoItem):
    django_model = Article


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, NewsWebsite):
        if instance.scraper_runtime:
            instance.scraper_runtime.delete()

    if isinstance(instance, Article):
        if instance.checker_runtime:
            instance.checker_runtime.delete()


pre_delete.connect(pre_delete_handler)
