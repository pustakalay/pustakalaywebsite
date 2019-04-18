from django.conf.urls import url
from booksapp.views import UserProductHistoryView
from .views import (
        AccountHomeView, 
        UserDetailUpdateView,
        )

urlpatterns = [
    url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
    url(r'history/books/$', UserProductHistoryView.as_view(), name='user-book-history'),
    url(r'^$', AccountHomeView.as_view(), name='home'),    
]