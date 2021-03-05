import requests
from django.conf import settings

def send_otp(text, phone_number):
    body = settings.OTP_SPARROW['BODY']
    body['to'] = phone_number
    body['text'] = text
    print("Body: {0}".format(body))
    response = requests.post(
            settings.OTP_SPARROW['POST_URL'],
            data=body)
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


def split_full_name(full_name):
    full_name_dict = dict()
    full_name_list = [word for word in full_name.split(" ") if word]
    first_name = full_name_list[0]
    last_name = full_name_list[-1]
    middle_name_list = full_name_list[1:-1]
    middle_name=""
    for word in middle_name_list:
        middle_name += word + " "
    full_name_dict['first_name']=first_name
    full_name_dict['middle_name']=middle_name
    full_name_dict['last_name']=last_name
    return full_name_dict
