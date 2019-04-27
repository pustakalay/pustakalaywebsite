from django.http import HttpResponse, JsonResponse
import requests
from pustakalaywebsite.settings import MSG91_AUTH_KEY, IS_SMS_SIMULATED

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
    payload = {'authkey': MSG91_AUTH_KEY,
                'mobile': request.POST.get("phone-number"),
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
    return HttpResponse(data)