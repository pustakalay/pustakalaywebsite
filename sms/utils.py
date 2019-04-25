import requests
from pustakalaywebsite.settings import MSG91_AUTH_KEY

def send_transactional_sms(mobiles,message):
    payload = {'authkey': MSG91_AUTH_KEY,
                'mobiles': mobiles,
                'route': '4',
                'message':message,
                'sender' : 'PSTKLY',
                'country' : '91',
    }
    response = requests.post('http://api.msg91.com/api/v2/sendsms', params=payload)
    print(payload)
#     print(response.json())
#     data = response.json()
    data = {
          "message":"3763646c3058373530393938",
          "type":"success"
        }
    return data

def verify_otp(mobile,otp):
#     payload = {'authkey': MSG91_AUTH_KEY, 'mobile': mobile, 'otp': otp}
#     response = requests.post('https://control.msg91.com/api/verifyRequestOTP.php', params=payload)
#     print(payload)
#     print(response.json())
#     data = response.json()
    data = {
      "message":"number_verified_successfully",
      "type":"error"
    }
    return data

def send_otp(mobile):
#         payload = {'authkey': MSG91_AUTH_KEY,
#                 'mobile': mobile,
#                 'otp_length': '4',
#                 'message':'Welcome to Pustakalay. Your OTP is ##OTP##.',
#                 'sender' : 'PSTKLY',
#                 'otp_expiry' : '10',
#         }
#         response = requests.post('http://control.msg91.com/api/sendotp.php', params=payload)
#         print(payload)
#         print(response.json())
#         data = response.json()
        data = {
          "message":"3763646c3058373530393938",
          "type":"success"
        }
        return data     
    