from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import *


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # проверка пользователя
        if user is not None:
            login(request, user)

            next_url = request.GET.get('next', 'index')  # переход на следующую страницу
            return redirect(next_url)

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'index.html')


def create_supply(request):
    SuppliesItemsFormSet = inlineformset_factory(Supplies, SuppliesItems, fields=('product', 'quantity'), extra=1)

    if request.method == 'POST':
        supplies_form = SuppliesForm(request.POST)
        supplies_items_formset = SuppliesItemsFormSet(request.POST)

        print(supplies_items_formset)

        if supplies_form.is_valid() and supplies_items_formset.is_valid():
            supplies = supplies_form.save()
            supplies_items_formset.instance = supplies
            supplies_items_formset.save()
            return redirect('supply_list')
    else:
        supplies_form = SuppliesForm()
        supplies_items_formset = SuppliesItemsFormSet()

    return render(request, 'create_order.html',
                  {'supplies_form': supplies_form, 'supplies_items_formset': supplies_items_formset})


def supply_list(request):
    supplies = Supplies.objects.all()
    return render(request, 'supply_list.html', {'supplies': supplies})


def filials(request):
    filials = Filials.objects.all()
    return render(request, 'filials.html', {'filials': filials})


def products(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'products': products})


def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})


def write_offs(request, pk):
    write_offs = Write_offs.objects.filter(filial=pk)
    return render(request, 'write_offs.html', {'write_offs': write_offs})


def sales(request, pk):
    sales = Sales.objects.filter(filial=pk)
    total_cost = 0
    for sale in sales:
        total_cost += sale.cost
    return render(request, 'sales.html', {'sales': sales, 'total_cost': total_cost})
