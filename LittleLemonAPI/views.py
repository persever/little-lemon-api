from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import auth_login, auth_logout
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import CartItem, Category, MenuItem, Order, Rating
from .paginators import MenuPagination
from .permissions import is_crew, is_customer, is_manager, IsAdminOrManager, IsCrew, IsManager
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, RatingSerializer

from .view_helpers.group_helper import group_helper
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
    queryset = Order.objects.select_related('menu_item').all()
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
            return Order.objects.select_related('menu_item').all()
        if is_crew(req):
            return Order.objects.select_related('menu_item').filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def update(self, req, *args, **kwargs):
        status = req.data.get('status')
        if status and status.lower() != 'delivered':
            raise ValidationError(message='"status" field may only be updated to "delivered". When an order is created, the default status is "pending" and when a Delivery crew is assigned it automatically updates to "assigned".', code='invalid')

        kwargs['partial'] = True
        return super().update(req, *args, **kwargs)

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(req, total):
    Order.objects.create(total=round(float(total), 2),user=req.user)
    return redirect('orders')

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(req, menu_item_id=None):
    if req.method == 'POST':
        if menu_item_id:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        else:
            menu_item_title = req.data.get('menu_item_title')
            menu_item = MenuItem.objects.get(title=menu_item_title)

        cart_item, created = CartItem.objects.get_or_create(
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
    total = 0
    total_after_tax = 0
    for item in items:
        total += item.menu_item.price
        total_after_tax += MenuItemSerializer.calculate_tax(MenuItem, item.menu_item)

    return render(
        request=req,
        template_name='cart.html',
        context={
            'cart_is_empty': len(items) == 0,
            'items': items,
            'tax': total_after_tax - total,
            'total': total,
            'total_after_tax': total_after_tax,
            'username': req.user.username
        }
    )

@api_view(['DELETE','GET','POST'])
@permission_classes([IsAdminUser])
def manager(req):
    return group_helper(req, 'Manager', 'managers')

@api_view(['DELETE','GET','POST'])
@permission_classes([IsAdminOrManager])
def crew(req):
    return group_helper(req, 'Delivery crew', 'crew')

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