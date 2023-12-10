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

def success_resp(data={}):
    return Response({'message':'Success!','data': {**data}}, status.HTTP_200_OK)

@api_view()
def menu(req):
    items = MenuItem.objects.select_related('category').all()
    
    category_name = req.query_params.get('category')
    if category_name:
        items = items.filter(category__title=category_name)
    
    to_price = req.query_params.get('to_price')
    if to_price:
        items = items.filter(price=to_price)
    
    search = req.query_params.get('search')
    if search:
        items = items.filter(title__contains=search)

    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-items.html')

@api_view()
@permission_classes([IsAuthenticated])
def secret(req):
    return Response({'message':'This is the secret message!'}, status.HTTP_200_OK)

@api_view(['DELETE','GET','POST'])
@permission_classes([IsAdminUser])
def manager(req):
    managers = Group.objects.get(name='Manager')

    username = req.data.get('username')
    if username:
        user = get_object_or_404(User, username=username)
        try:
            if req.method == 'POST':
                managers.user_set.add(user)
            elif req.method == 'DELETE':
                managers.user_set.remove(user)
        except Exception as e:
            raise e

    manager_users = User.objects.filter(groups__name='Manager')
    managers_list = []
    for manager in manager_users.values():
        managers_list.append(manager['username'])

    return success_resp({'managers':managers_list})

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(req):
    return success_resp()
        
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(req):
    return success_resp()