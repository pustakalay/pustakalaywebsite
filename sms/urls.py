from django.conf.urls import url
from .views import resend_otp, check_balance


urlpatterns = [
    url(r'^check-balance/$', check_balance, name='check-balance'),
    url(r'^resend-otp/$', resend_otp, name='resend-otp'),
    ]