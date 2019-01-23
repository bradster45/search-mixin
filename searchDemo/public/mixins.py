import re

from django.db.models import Q


# base search mixin
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


# simple icontains mixin. simply runs icontains filter on search vectors
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


# full text search. matches multiple fields in an 'or' case. if search matches one or more fields, object is in the queryset
class FullTextSearchMixin(SearchMixin):
    """
    This mixin will perform a full text search on this app's article lists.
    If postgres is not used it will do a slower icontains search
    on the relevant fields annotating a similar rank.
    """

    # matches words with an 'or' case. if one or more word is in the searchable fields, object is a match
    # def get_queryset(self, ):
    #     qs = super(FullTextSearchMixin, self).get_queryset()
    #     q = self.request.GET.get('q')
    #     if q is not None and q != '':
    #         # split the words by whitespace and remove any below 3 characters
    #         self.query_words = [
    #             word for word in re.findall(r'\w+', q) if len(word) > 2
    #         ]
    #         if len(self.query_words) > 0:
    #             search_query = None
    #             for vector in self.search_vector:
    #                 for word in self.query_words:
    #                     if search_query is None:
    #                         search_query = Q(**{vector + "__icontains": word})
    #                     else:
    #                         search_query = search_query | Q(**{vector + "__icontains": word})
    #             return qs.filter(search_query).distinct()
    #     return qs

    # matches words with an 'and' case. if all search words are in a searchable field, object is a match
    def get_queryset(self, ):
        qs = super(FullTextSearchMixin, self).get_queryset()
        q = self.request.GET.get('q')
        if q is not None and q != '':
            # split the words by whitespace and remove any below 3 characters
            self.query_words = [
                word for word in re.findall(r'\w+', q) if len(word) > 2
            ]
            if len(self.query_words) > 0:
                # search_query gets evaluated with an or case
                search_query = None
                for vector in self.search_vector:
                    # mini queries get evaluated with an and case
                    mini_query = None
                    for word in self.query_words:
                        if mini_query is None:
                            mini_query = Q(**{vector + "__icontains": word})
                        else:
                            mini_query = mini_query & Q(**{vector + "__icontains": word})
                    if search_query is None:
                        search_query = mini_query
                    else:
                        search_query = search_query | mini_query
                return qs.filter(search_query).distinct()
        return qs.distinct()

