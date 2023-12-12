from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:menu_item_id>', views.cart, name='add_to_cart'),

    path('categories/', views.CategoriesViewSet.as_view({'get':'list','post':'create'})),
    path('categories/<int:pk>', views.CategoriesViewSet.as_view({'get':'retrieve'})),

    path('menu-items/', views.MenuItemsViewSet.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>', views.MenuItemsViewSet.as_view({'get':'retrieve','patch':'partial_update'})),
    
    path('orders/', views.OrdersViewSet.as_view({'get':'list','post':'create'}), name="orders"),
    path('orders/new/<str:total>', views.place_order, name="place_order"),
    path('orders/<int:pk>', views.OrdersViewSet.as_view({'get':'retrieve','patch':'partial_update'})),

    path('ratings/', views.RatingsViewSet.as_view({'get':'list','post':'create'})),
    path('ratings/<int:pk>', views.RatingsViewSet.as_view({'get':'retrieve'})),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout),
    path('register/', views.register),

    path('groups/manager/users/', views.manager),
    path('groups/crew/users/', views.crew),

]
