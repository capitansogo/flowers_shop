from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('filials/', views.filials, name='filials'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('orders/<int:pk>/', views.orders, name='orders'),
    path('create_supply/<int:pk>/', views.create_supply, name='create_supply'),
    path('supply-list/', views.supply_list, name='supply_list'),
    path('write_offs/<int:pk>/', views.write_offs, name='write_offs'),
    path('sales/<int:pk>/', views.sales, name='sales'),
    path('create_service_order/<int:pk>/', views.create_service_order, name='create_service_order'),
    path('create_order/<int:pk>/', views.create_order, name='create_order'),
    path('register/', views.register, name='register'),
    path('supplies/<int:pk>/', views.supplies, name='supplies'),
    path('all_supplies/', views.all_supplies, name='all_supplies'),
    path('all_write_offs/', views.all_write_offs, name='all_write_offs'),
    path('all_sales/', views.all_sales, name='all_sales'),
    path('all_orders/', views.all_orders, name='all_orders'),


]
