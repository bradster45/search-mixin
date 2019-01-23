# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from public.models import Article, Page

admin.site.register(Article)
admin.site.register(Page)
