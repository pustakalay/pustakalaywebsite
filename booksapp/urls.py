from .views import BookListView, BookDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', BookListView.as_view(), name='bookslist'),
    url(r'^(?P<slug>[\w-]+)/$', BookDetailView.as_view(), name='booksdetail'),
]
