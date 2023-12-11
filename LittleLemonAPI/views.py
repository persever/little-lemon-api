from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

from .models import MenuItem, Category, Rating
from .serializers import MenuItemSerializer, CategorySerializer, RatingSerializer
from .helpers.view_helpers import success_resp, bad_req_resp

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

    filterset_fields=['featured']
    ordering_fields=['price']
    search_fields=['title', 'category__title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method == 'POST' or self.request.method == 'PATCH':
            if self.request.user.groups.filter(name='Manager').exists():
                return [BasePermission()]
            else:
                return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def update(self, req, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(req, *args, **kwargs)

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

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