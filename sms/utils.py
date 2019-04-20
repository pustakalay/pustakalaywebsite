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
#     response = requests.post('http://api.msg91.com/api/v2/sendsms', params=payload)
    print(payload)
#     print(response.json())
#     data = response.json()
    data = {
          "message":"3763646c3058373530393938",
          "type":"success"
        }
    return data
