from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('filials/', views.filials, name='filials'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('create_supply/', views.create_supply, name='create_order'),
    path('supply-list/', views.supply_list, name='supply_list'),
    path('write_offs/<int:pk>/', views.write_offs, name='write_offs'),
    path('sales/<int:pk>/', views.sales, name='sales'),
]
