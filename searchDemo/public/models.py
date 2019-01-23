# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify


@python_2_unicode_compatible
class AutoSluggedAbstractModel(models.Model):
    # abstract model for unique title and slug fields
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=256)

    class Meta:
        abstract = True

    def __str__(self, ):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        super(AutoSluggedAbstractModel, self).save(*args, **kwargs)


class Article(AutoSluggedAbstractModel):
    pass


class Page(AutoSluggedAbstractModel):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='pages')
    body = models.TextField(max_length=600)
    number = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        page_last = self.article.pages.last()
        if page_last and page_last.number > 0:
            self.number = page_last.number + 1
        super(Page, self).save(*args, **kwargs)

