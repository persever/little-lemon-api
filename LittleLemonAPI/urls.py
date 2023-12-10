from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesViewSet.as_view({'get':'list','post':'create'})),
    path('categories/<int:pk>', views.CategoriesViewSet.as_view({'get':'retrieve'})),
    path('groups/manager/users/', views.manager),
    path('menu-items/', views.MenuItemsViewSet.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>', views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('ratings/', views.RatingsViewSet.as_view({'get':'list','post':'create'})),
    path('ratings/<int:pk>', views.RatingsViewSet.as_view({'get':'retrieve'})),
    path('secret', views.secret),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
]
