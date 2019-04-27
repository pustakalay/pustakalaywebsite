import requests
from pustakalaywebsite.settings import MSG91_AUTH_KEY, IS_SMS_SIMULATED

def send_transactional_sms(mobiles,message):
    payload = {'authkey': MSG91_AUTH_KEY,
                'mobiles': mobiles,
                'route': '4',
                'message':message,
                'sender' : 'PSTKLY',
                'country' : '91',
    }
    if not IS_SMS_SIMULATED:
        response = requests.post('http://api.msg91.com/api/v2/sendsms', params=payload)
        data = response.json()
    else:
        data = {
              "message":"3763646c3058373530393938",
              "type":"success"
            }
    print(payload)
    print(data)
    return data

def verify_otp(mobile,otp):
    payload = {'authkey': MSG91_AUTH_KEY, 'mobile': mobile, 'otp': otp}
    if not IS_SMS_SIMULATED:
        response = requests.post('https://control.msg91.com/api/verifyRequestOTP.php', params=payload)
        data = response.json()
    else:
        data = {
          "message":"number_verified_successfully",
          "type":"success"
        }
    print(payload)
    print(data)
    return data

def send_otp(mobile):
        payload = {'authkey': MSG91_AUTH_KEY,
                'mobile': mobile,
                'otp_length': '4',
                'message':'Welcome to Pustakalay. Your OTP is ##OTP##. OTP will expire in 10 mins.',
                'sender' : 'PSTKLY',
                'otp_expiry' : '10',
        }
        if not IS_SMS_SIMULATED:
            response = requests.post('http://control.msg91.com/api/sendotp.php', params=payload)
            data = response.json()
        else:
            data = {
              "message":"3763646c3058373530393938",
              "type":"success"
            }
        print(payload)
        print(data)
        return data     
    