from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from .responses import success_resp, bad_req_resp

def group_helper(req, groupname, data_key):
    group = Group.objects.get(name=groupname)
    members = User.objects.filter(groups__name=groupname)

    membere_names = set()
    for member in members.values():
        membere_names.add(member['username'])

    message=''
    data={f'{data_key}':membere_names}
    http_status=status.HTTP_200_OK

    username = req.data.get('username')
    if username:
        try:
            user = get_object_or_404(User, username=username)
            if req.method == 'POST':
                if username in membere_names:
                    return bad_req_resp(f'User {username} is already in the {groupname} group.')
                else:
                    group.user_set.add(user)
                    message=f'User {username} was assigned to the {groupname} group.'
                    data = None
                    http_status=status.HTTP_201_CREATED
            elif req.method == 'DELETE':
                if username not in membere_names:
                    return bad_req_resp(f'User {username} is not in the {groupname} group.')
                else:
                    group.user_set.remove(user)
                    message=f'User {username} was removed from the {groupname} group.'
                    data = None
        except Exception as e:
            raise e

    return success_resp(message, data, http_status)