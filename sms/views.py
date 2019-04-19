from django.http import HttpResponse, JsonResponse
import requests
from pustakalaywebsite.settings import MSG91_AUTH_KEY

def check_balance(request):
    payload = {'authkey': MSG91_AUTH_KEY, 'type': '4'}
    response = requests.get('http://control.msg91.com/api/balance.php', params=payload)
    if request.is_ajax():
        data = {
            "number": response.text
        }
        return JsonResponse(data)
    return HttpResponse(response.text)

def verify_otp(request):
#     payload = {'authkey': MSG91_AUTH_KEY, 'mobile': request.POST.get("phone-number"), 'otp': request.POST.get("otp-number")}
#     response = requests.post('https://control.msg91.com/api/verifyRequestOTP.php', params=payload)
#     print(payload)
#     print(response.json())
#     data = response.json()
    data = {
      "message":"number_verified_successfully",
      "type":"success"
    }
    if request.is_ajax():
        return JsonResponse(data)
    return HttpResponse(data)

def send_otp(request):
#     payload = {'authkey': MSG91_AUTH_KEY,
#                 'mobile': request.POST.get("phone-number"),
#                 'otp_length': '4',
#                 'message':'Welcome to Pustakalay. Your OTP is ##OTP##.',
#                 'sender' : 'PSTKLY',
#                 'otp_expiry' : '10',
#     }
#     response = requests.post('http://control.msg91.com/api/sendotp.php', params=payload)
#     print(payload)
#     print(response.json())
#     data = response.json()
    data = {
          "message":"3763646c3058373530393938",
          "type":"success"
        }
    if request.is_ajax():
        return JsonResponse(data)
    return HttpResponse(data)