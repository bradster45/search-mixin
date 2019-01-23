from django.conf.urls import url
from public.views import ArticleList, ArticleDetail

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='articles'),
    url(r'^article/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article'),
]
