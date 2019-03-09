from .views import cart_home
from django.conf.urls import url

urlpatterns = [
    url(r'^$', cart_home, name='cart'),
]
