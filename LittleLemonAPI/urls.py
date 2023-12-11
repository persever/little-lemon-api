from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from . import views

urlpatterns = [
    path('categories/', views.CategoriesViewSet.as_view({'get':'list','post':'create'})),
    path('categories/<int:pk>', views.CategoriesViewSet.as_view({'get':'retrieve'})),
    path('groups/manager/users/', views.manager),
    path('groups/crew/users/', views.crew),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout),
    path('menu-items/', views.MenuItemsViewSet.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>', views.MenuItemsViewSet.as_view({'get':'retrieve','patch':'partial_update'})),
    path('orders/', views.OrdersViewSet.as_view({'get':'list','post':'create'})),
    path('orders/<int:pk>', views.OrdersViewSet.as_view({'get':'retrieve','patch':'partial_update'})),
    path('ratings/', views.RatingsViewSet.as_view({'get':'list','post':'create'})),
    path('ratings/<int:pk>', views.RatingsViewSet.as_view({'get':'retrieve'})),
    path('register/', views.register),
]
