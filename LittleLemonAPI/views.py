from django.contrib.auth.models import User, Group
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import MenuItem, Category, Rating
from .serializers import MenuItemSerializer, CategorySerializer, RatingSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    ordering_fields=['price','inventory']
    search_fields=['title','category__title']

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

def success_resp(message='', data={}):
    if message:
        message = ' ' + message
    return Response({'message':'Success!' + message,'data': {**data}}, status.HTTP_200_OK)

def bad_req_resp(message='', data={}):
    if message:
        message = ' ' + message
    return Response({'message':'Bad request.' + message,'data': {**data}}, status.HTTP_400_BAD_REQUEST)

# @api_view()
# def menu(req):
#     items = MenuItem.objects.select_related('category').all()
    
#     category_name = req.query_params.get('category')
#     if category_name:
#         items = items.filter(category__title=category_name)
    
#     to_price = req.query_params.get('to_price')
#     if to_price:
#         items = items.filter(price=to_price)
    
#     search = req.query_params.get('search')
#     if search:
#         items = items.filter(title__contains=search)

#     serialized_item = MenuItemSerializer(items, many=True)
#     return Response({'data':serialized_item.data}, template_name='menu-items.html')

@api_view()
@permission_classes([IsAuthenticated])
def secret(req):
    return Response({'message':'This is the secret message!'}, status.HTTP_200_OK)

@api_view(['DELETE','GET','POST'])
@permission_classes([IsAdminUser])
def manager(req):
    manager_group = Group.objects.get(name='Manager')
    manager_users = User.objects.filter(groups__name='Manager')

    manager_names = set()
    for manager in manager_users.values():
        manager_names.add(manager['username'])

    message=''

    username = req.data.get('username')
    if username:
        try:
            user = get_object_or_404(User, username=username)
            if req.method == 'POST':
                if username in manager_names:
                    return bad_req_resp(f'User {username} is already in the Manager group.')
                else:
                    manager_group.user_set.add(user)
                    message=f'User {username} was assigned to the Manager group.'
            elif req.method == 'DELETE':
                if username not in manager_names:
                    return bad_req_resp(f'User {username} is not in the Manager group.')
                else:
                    manager_group.user_set.remove(user)
                    message=f'User {username} was removed from the Manager group.'
        except Exception as e:
            raise e

    return success_resp(message, {'managers':manager_names})

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(req):
    return success_resp()
        
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(req):
    return success_resp()