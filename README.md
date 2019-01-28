# searchMixin
Django search mixin

A simple series of Django mixin classes to apply to a ListView that filters the queryset based on a user search.

### Key bits of code are as follows.

1) Mixin to inherit from  in ListView
[FullTextSearchMixin](https://github.com/bradster45/searchMixin/blob/master/searchDemo/public/mixins.py#L49)

2) ListView that inherits from mixin, and has a search_vector array defined in the class
[ArticleList](https://github.com/bradster45/searchMixin/blob/master/searchDemo/public/views.py#L13)

Note the 'search_vector' array. These are the model fields you wish to search using the mixin.

3) The HTML form that generates the url args used by the mixin in order to filter
[#search_form](https://github.com/bradster45/searchMixin/blob/master/searchDemo/public/templates/public/base.html#L27)
