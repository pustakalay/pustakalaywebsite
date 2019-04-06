from django.conf.urls import url
from .views import (
    AddressCreateView,
    AddressListView,
    AddressUpdateView,
    checkout_address_create_view, 
    checkout_address_reuse_view
    )

urlpatterns = [
    url(r'^$', AddressListView.as_view(), name='home'),
    url(r'^create/$', AddressCreateView.as_view(), name='address-create'),
    url(r'^(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
    url(r'^address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
]