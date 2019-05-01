from django.http import HttpResponse, JsonResponse
import requests
from pustakalaywebsite.settings import MSG91_AUTH_KEY, IS_SMS_SIMULATED
from django.urls import reverse
from django.shortcuts import redirect 

def check_balance(request):
    payload = {'authkey': MSG91_AUTH_KEY, 'type': '4'}
    response = requests.get('http://control.msg91.com/api/balance.php', params=payload)
    if request.is_ajax():
        data = {
            "number": response.text
        }
        return JsonResponse(data)
    return HttpResponse(response.text)

def resend_otp(request):
    phone_number = request.session.get("otp-phone-number", None)
    if request.is_ajax():
        phone_number = request.POST.get("phone-number")
    payload = {'authkey': MSG91_AUTH_KEY,
                'mobile': phone_number,
    }
    if not IS_SMS_SIMULATED:
        response = requests.post('http://control.msg91.com/api/retryotp.php', params=payload)
        data = response.json()
    else:
        data = {
          "message":"otp_sent_successfully",
          "type":"success"
        }
    print(payload)
    print(data)
    if request.is_ajax():
        return JsonResponse(data)
    url = reverse('register_page', kwargs={'phonenumber': phone_number})  
    return redirect(url)