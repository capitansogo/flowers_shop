from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_supply/', views.create_supply, name='create_order'),
    path('supply-list/', views.supply_list, name='supply_list'),
]
