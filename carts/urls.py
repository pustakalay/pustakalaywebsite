from .views import cart_home, cart_update, checkout_home
from django.conf.urls import url

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', cart_update, name='update'),
]
