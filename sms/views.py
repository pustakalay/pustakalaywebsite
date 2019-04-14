from django.http import HttpResponse
import requests

def check_balance(request):
    payload = {'authkey': '271679AzBM8Hzhz7K85cacf0f4', 'type': '4'}
    response = requests.get('http://control.msg91.com/api/balance.php', params=payload)
    return HttpResponse(response.text)

def verify_otp(request):
    pass
