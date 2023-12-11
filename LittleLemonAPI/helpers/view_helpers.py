from rest_framework import status
from rest_framework.response import Response

def create_resp_obj(message_prefix, message, data=None):
    if message:
        message = ' ' + message
    resp_obj = {'message': message_prefix + ' ' + message}
    if data != None:
        resp_obj['data'] = {**data}
    return resp_obj

def success_resp(message='', data=None, http_status=status.HTTP_200_OK):
    resp_obj = create_resp_obj('Success!', message, data)
    return Response(resp_obj, status=http_status)

def bad_req_resp(message='', data=None, http_status=status.HTTP_400_BAD_REQUEST):
    resp_obj = create_resp_obj('Bad request.', message, data)
    return Response(resp_obj, status=http_status)