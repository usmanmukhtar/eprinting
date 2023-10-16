from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta

def specific_object_error_response(message):
    return Response({"data": {}, "success": False, "message": message, "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST)

def error_response(serializer):
    message = "\n".join(
        f"{key} field is required" if "required" in value[0] else f"{value[0]}" for key, value in
        serializer.errors.items())
    return Response({"data": serializer.errors, "success": False, "message": message, "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST)

def success_response(serializer, message, status_code=200, send_data=True):
    response = {'success': True, 'message': message, "status_code": status_code,'data': serializer.data if send_data else {}}
    return Response(response, status=status_code)

def success_response_message(data, message, status_code=200, send_data=True):

    response = {'success': True, 'message': message, "status_code": status_code,'data': data if send_data else {}}
    return Response(response, status=status_code)

def specific_error_response(message):
    return Response({"data": {}, "success": False, "message": message, "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST)


import base64
import hashlib
import hmac
from django.conf import settings

# def calc_signature_from_str(s, secret):
def calc_signature_from_str(action_name):
    byte_key = bytes(secret_key, 'utf-8')
    lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
    # timestamp = "221013185003"
    timestamp = datetime.now() + timedelta(hours=5)
    timestamp = timestamp.strftime("%y%m%d%H%M%S")
    print("timestamp : ", timestamp)
    s = '{}/{}/1.1/2.0/HmacSHA256/{}+0200/JSON'.format(action_name,api_key,timestamp)
    lhmac.update(s.encode('utf8'))
    signature = base64.b64encode(lhmac.digest())
    print("signat : ", signature)
    decoded_signature = signature.decode("utf-8").rstrip('=').replace('+','-').replace('/','_')
    print("decode : ", decoded_signature)

    link = '{}/{}/1.1/2.0/HmacSHA256/{}/{}+0200/JSON'.format(action_name,api_key,decoded_signature,timestamp)

    print("new link is : ",link)
    return link