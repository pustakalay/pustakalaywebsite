from django.conf.urls import url
from .views import check_balance


urlpatterns = [
    url(r'^check-balance/$', check_balance, name='check-balance'),
    
    ]