from django.conf.urls import url
from .views import verify_otp, send_otp, check_balance


urlpatterns = [
    url(r'^check-balance/$', check_balance, name='check-balance'),
    url(r'^send-otp/$', send_otp, name='send-otp'),
    url(r'^verify-otp/$', verify_otp, name='verify-otp'),
    ]