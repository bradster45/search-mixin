# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from public.models import Article
from public.mixins import FullTextSearchMixin


# full text search. will search article title, and the article's pages' body field for the query string
# it will return any articles that matches either field
class ArticleList(FullTextSearchMixin, ListView):
    model = Article
    search_vector = ['title', 'pages__body']
    paginate_by = 20


class ArticleDetail(DetailView):
    model = Article