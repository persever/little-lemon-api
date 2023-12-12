from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import auth_login, auth_logout
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import CartItem, Category, MenuItem, Order, Rating
from .paginators import MenuPagination
from .permissions import is_crew, is_customer, is_manager, IsCrew, IsManager
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, RatingSerializer

from .view_helpers.responses import success_resp, bad_req_resp
from .view_helpers.validators import is_valid_single_field_req

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

    filterset_fields=['category__title', 'featured']
    ordering_fields=['price']
    ordering=['category__title']
    pagination_class=MenuPagination
    search_fields=['title', 'category__title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method == 'PATCH' or self.request.method == 'POST':
            if is_valid_single_field_req(self, 'featured') == True:
                return [IsManager()]
            else:
                return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def list(self, req):
        if is_customer(req):
            results = self.get_queryset()

            category = req.GET.get('category')
            if (category):
                case_corrected_category_query = category[0].upper() + category[1::]
                results = results.filter(category__title=case_corrected_category_query)

            sortby = req.GET.get('sortby') or req.GET.get('ordering')
            if (sortby):
                results = results.order_by(sortby)

            page = req.GET.get('page')
            if (page != None):
                paginated = Paginator(results, 4)
                results = paginated.get_page(page)

            return render(
                request=req,
                template_name='menu.html',
                context={
                    'results': results,
                    'user_is_authenticated': req.user.is_authenticated,
                    'no_results_found': len(results) == 0
                }
            )

        return super().list(req)

    def update(self, req, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(req, *args, **kwargs)

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            if (is_valid_single_field_req(self, 'delivery_crew') == True):
                return [IsManager()]
            elif (is_valid_single_field_req(self, 'status') == True):
                return [IsCrew()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAdminUser()]
    
    def get_queryset(self):
        req = self.request
        user = req.user
        if user.is_superuser or is_manager(req):
            return self.queryset
        if is_crew(req):
            return self.queryset.filter(delivery_crew=user)
        return self.queryset.filter(user=user)

    def update(self, req, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(req, *args, **kwargs)

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(req):
    if req.method == 'POST':
        menu_item_id = req.GET.get('menu_item_id')
        if menu_item_id:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        else:
            menu_item_title = req.data.get('menu_item_title')
            menu_item = MenuItem.objects.get(title=menu_item_title)

        cart_item, create = CartItem.objects.get_or_create(
            menu_item=menu_item,
            user=req.user,
        )
        cart_item.quantity += 1
        cart_item.save()

        return redirect('cart')

    elif req.method == 'DELETE':
        menu_item_title = req.data.get('menu_item_title')
        menu_item = MenuItem.objects.get(title=menu_item_title)
        cart_item = CartItem.objects.get(menu_item=menu_item)
        cart_item.delete()

    items = CartItem.objects.select_related('menu_item').filter(user=req.user)
    total = round(sum(item.menu_item.price * item.quantity for item in items), 2)

    return render(
        request=req,
        template_name='cart.html',
        context={
            'cart_is_empty': len(items) == 0,
            'items': items,
            'total': total,
            'username': req.user.username
        }
    )

@api_view(['DELETE','GET','POST'])
@permission_classes([IsAdminUser])
def manager(req):
    manager_group = Group.objects.get(name='Manager')
    manager_users = User.objects.filter(groups__name='Manager')

    manager_names = set()
    for manager in manager_users.values():
        manager_names.add(manager['username'])

    message=''
    data={'managers':manager_names}
    http_status=status.HTTP_200_OK

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
                    data = None
                    http_status=status.HTTP_201_CREATED
            elif req.method == 'DELETE':
                if username not in manager_names:
                    return bad_req_resp(f'User {username} is not in the Manager group.')
                else:
                    manager_group.user_set.remove(user)
                    message=f'User {username} was removed from the Manager group.'
                    data = None
        except Exception as e:
            raise e

    return success_resp(message, data, http_status)

# This and the above view 'manager' should be refactored
# to use shared functions in order to keep the code DRY.
@api_view(['DELETE','GET','POST'])
@permission_classes([IsManager])
def crew(req):
    crew_group = Group.objects.get(name='Delivery crew')
    crew_users = User.objects.filter(groups__name='Delivery crew')

    crew_names = set()
    for crew in crew_users.values():
        crew_names.add(crew['username'])

    message=''
    data={'crew':crew_names}
    http_status=status.HTTP_200_OK

    username = req.data.get('username')
    if username:
        try:
            user = get_object_or_404(User, username=username)
            if req.method == 'POST':
                if username in crew_names:
                    return bad_req_resp(f'User {username} is already in the Delivery crew group.')
                else:
                    crew_group.user_set.add(user)
                    message=f'User {username} was assigned to the Delivery crew group.'
                    data = None
                    http_status=status.HTTP_201_CREATED
            elif req.method == 'DELETE':
                if username not in crew_names:
                    return bad_req_resp(f'User {username} is not in the Delivery crew group.')
                else:
                    crew_group.user_set.remove(user)
                    message=f'User {username} was removed from the Delivery crew group.'
                    data = None
        except Exception as e:
            raise e

    return success_resp(message, data, http_status)

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            success_resp('Registration successful.')

        bad_req_resp('Unsuccessful registration.')

    form = UserCreationForm()
    return render(
        request=req,
        template_name='register.html',
        context={'register_form': form}
    )

def logout(req):
    if req.method == 'POST':
        auth_logout(req)
    return render(
        request=req,
        template_name='logout.html'
    )