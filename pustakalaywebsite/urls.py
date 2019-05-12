"""pustakalaywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from .views import home_page, contact_page, update_pincode
from accounts.views import LoginView, RegisterView
from django.contrib.auth import views as auth_views
from carts.views import cart_detail_api_view
from django.views.generic import RedirectView
from accounts.views import send_otp_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home'),
    url(r'^update-pincode/$', update_pincode, name='update-pincode'),
    url(r'^sms/', include("sms.urls", namespace='sms')),
    url(r'^orders/', include("orders.urls", namespace='orders')),
    url(r'^address/$', RedirectView.as_view(url='/addresses')),
    url(r'^addresses/', include("addresses.urls", namespace='addresses')),
    url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include("accounts.urls", namespace='account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^register/(?P<phonenumber>\d+)/$', RegisterView.as_view(), name='register_page'),
    url(r'^sendotp/$', send_otp_view, name='send-otp'),
    url(r'^contact/$', contact_page, name='contact'),
    url('books/', include('booksapp.urls', namespace='books')),
    url('search/', include('search.urls', namespace='search')),
    url('cart/', include('carts.urls', namespace='carts')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
