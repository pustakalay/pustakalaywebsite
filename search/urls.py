from .views import SearchBookListView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', SearchBookListView.as_view(), name='search'),
]
