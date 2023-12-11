from rest_framework import status
from rest_framework.response import Response

def success_resp(message='', data={}, status=status.HTTP_200_OK):
    if message:
        message = ' ' + message
    return Response({'message':'Success!' + message,'data': {**data}}, status)

def bad_req_resp(message='', data={}):
    if message:
        message = ' ' + message
    return Response({'message':'Bad request.' + message,'data': {**data}}, status.HTTP_400_BAD_REQUEST)