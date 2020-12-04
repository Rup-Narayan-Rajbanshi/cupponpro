import requests
from django.conf import settings

def send_otp(text, phone_number):
    body = settings.OTP_SPARROW['BODY']
    body['to'] = phone_number
    body['text'] = text
    print("Body: {0}".format(body))
    response = requests.post(
            settings.OTP_SPARROW['POST_URL'],
            params=body)
    response_json = response.json()
    message = ''
    if response.status_code == 200:
        message = "Code successfully sent to {0} for verification".format(phone_number)
        print(message)
        return True, message
    else:
        message = "Could not sent code to {0} " \
                  "for verification because of {1}".format(phone_number, response.text)
        print(message)
    return False, message
