import re

from django.db.models import Q
from django.views.generic.list import ListView


class SearchMixin(object):
    query_words = []  # strings to filter by
    search_vector = []  # model fields to be filtered

    def get_context_data(self, **kwargs):
        """
        add the query and query_words to the context
        """
        context = super(SearchMixin, self).get_context_data(**kwargs)
        # if anything meaningfull was searched
        q = self.request.GET.get('q', False)
        if q:
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
        if len(self.query_words) > 0:
            context['q'] = q
            context['query_words'] = self.query_words
        return context


class IcontainsSearchMixin(SearchMixin):
    def get_queryset(self, ):
        qs = super(IcontainsSearchMixin, self).get_queryset()
        q = self.request.GET.get('q')
        if q is not None and q != '':
            # split the words by whitespace and remove any below 3 characters
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
            if len(self.query_words) > 0:
                for vector in self.search_vector:
                    for word in self.query_words:
                        kwargs = {}
                        kwargs[vector + '__icontains'] = word
                        qs = qs.filter(**kwargs)
        return qs


class FullTextSearchMixin(SearchMixin):
    """
    This mixin will perform a full text search on this app's article lists.
    If postgres is not used it will do a slower icontains search
    on the relevant fields annotating a similar rank.
    """

    def get_queryset(self, ):
        qs = super(FullTextSearchMixin, self).get_queryset()
        q = self.request.GET.get('q')
        if q is not None and q != '':
            # split the words by whitespace and remove any below 3 characters
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
            if len(self.query_words) > 0:
                search_query = None
                for vector in self.search_vector:
                    for word in self.query_words:
                        if search_query is None:
                            search_query = Q(**{vector + "__icontains": word})
                        else:
                            search_query = search_query | Q(
                                **{vector + "__icontains": word})
                return qs.filter(search_query).distinct()
        return qs


# full text search. will search article title, and the article's pages' body field for the query string
# it will return any articles that matches either field
class ArticleListView(FullTextSearchMixin, ListView):
    model = Article
    search_vector = ['title', 'pages__body']