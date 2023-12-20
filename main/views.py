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


def supply_list(request):
    supplies = Supplies.objects.all()
    return render(request, 'supply_list.html', {'supplies': supplies})


def filials(request):
    filials = Filials.objects.all()
    return render(request, 'filials.html', {'filials': filials})


def products(request):
    filials = Filials.objects.all()
    products = Products.objects.all()
    return render(request, 'products.html', {'products': products, 'filials': filials})


def services(request):
    filials = Filials.objects.all()
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services, 'filials': filials})


def write_offs(request, pk):
    write_offs = Write_offs.objects.filter(filial=pk)
    return render(request, 'write_offs.html', {'write_offs': write_offs})


def sales(request, pk):
    sales = Sales.objects.filter(filial=pk)
    total_cost = 0
    for sale in sales:
        total_cost += sale.cost
    return render(request, 'sales.html', {'sales': sales, 'total_cost': total_cost})


def create_order(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        client = request.user
        filial = request.POST['filial']
        filial = Filials.objects.get(id=filial)
        registration_date = datetime.datetime.now()
        quantity = request.POST['product_count']
        if product.stock_balance < int(quantity):
            return render(request, 'products.html', {'error': 'Недостаточно товара на складе'})

        cost = product.cost * int(quantity)

        # уменьшение количества товара на складе
        product.stock_balance -= int(quantity)
        product.save()

        Product_order.objects.create(client=client, product=product, filial=filial, registration_date=registration_date,
                                     quantity=quantity, cost=cost)

        return render(request, 'products.html', {'success': 'Заказ успешно создан'})


def create_service_order(request, pk):
    service = Services.objects.get(id=pk)
    if request.method == 'POST':
        client = request.user
        filial = request.POST['filial']
        filial = Filials.objects.get(id=filial)
        registration_date = datetime.datetime.now()
        cost = service.cost
        date_completion = request.POST['date_completion']
        # проверка, что date_completion введена
        if date_completion == '':
            return render(request, 'services.html', {'error': 'Введите дату выполнения'})
        Service_order.objects.create(client=client, service=service, filial=filial, registration_date=registration_date,
                                     cost=cost, date_completion=date_completion)
        return render(request, 'services.html', {'success': 'Заказ успешно создан'})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.errors.get('username'):
            form.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
        if form.errors.get('password'):
            form.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
        if form.errors.get('first_name'):
            form.fields['first_name'].widget.attrs.update({'class': 'form-control is-invalid'})
        if form.errors.get('last_name'):
            form.fields['last_name'].widget.attrs.update({'class': 'form-control is-invalid'})
        if form.errors.get('email'):
            form.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.role = Roles.objects.get(name='Клиент')
            user.save()
            return redirect('login')

    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


def orders(request, pk):
    orders = Product_order.objects.filter(client=pk)
    services = Service_order.objects.filter(client=pk)
    print(len(orders), len(services))
    # если нет заказов
    if len(orders) == 0 and len(services) == 0:
        return render(request, 'orders.html', {'products_error': 'Нет заказов', 'services_error': 'Нет заказов'})
    elif len(orders) == 0:
        return render(request, 'orders.html', {'products_error': 'Нет заказов', 'services': services})
    elif len(services) == 0:
        return render(request, 'orders.html', {'orders': orders, 'services_error': 'Нет заказов'})

    else:
        return render(request, 'orders.html', {'orders': orders, 'services': services})


def all_orders(request):
    orders = Product_order.objects.all()
    services = Service_order.objects.all()
    it_all = True
    if len(orders) == 0 and len(services) == 0:
        return render(request, 'orders.html', {'products_error': 'Нет заказов', 'services_error': 'Нет заказов'})
    elif len(orders) == 0:
        return render(request, 'orders.html', {'products_error': 'Нет заказов', 'services': services, 'it_all': it_all})
    elif len(services) == 0:
        return render(request, 'orders.html', {'orders': orders, 'services_error': 'Нет заказов', 'it_all': it_all})

    else:
        return render(request, 'orders.html', {'orders': orders, 'services': services, 'it_all': it_all})


# создание поставки
def create_supply(request, pk):
    if request.method == 'POST':
        print(request.POST)
        product = Products.objects.get(id=pk)
        quantity = request.POST['product_count']
        filial = request.POST['filial']
        filial = Filials.objects.get(id=filial)
        delivery_date = request.POST['delivery_date']
        Supplies.objects.create(filial=filial,
                                delivery_date=delivery_date)

        supply = Supplies.objects.last()

        supply = Supplies.objects.get(id=supply.id)

        # увеличение количества товара на складе
        product.stock_balance += int(quantity)
        product.save()

        # создание поставки
        SuppliesItems.objects.create(supplies=supply,
                                     product=product,
                                     quantity=quantity)

        return render(request, 'products.html', {'success_supply': 'Поставка успешно создана'})


def supplies(request, pk):
    supplies = Supplies.objects.filter(filial=pk)
    # группировка поставок по дате
    supplies_group = {}
    for supply in supplies:
        if supply.delivery_date in supplies_group:
            supplies_group[supply.delivery_date].append(supply)
        else:
            supplies_group[supply.delivery_date] = [supply]

    return render(request, 'supplies.html', {'supplies_group': supplies_group})


def all_supplies(request):
    supplies = Supplies.objects.all()
    # группировка поставок по дате
    supplies_group = {}
    for supply in supplies:
        if supply.delivery_date in supplies_group:
            supplies_group[supply.delivery_date].append(supply)
        else:
            supplies_group[supply.delivery_date] = [supply]

    return render(request, 'supplies.html', {'supplies_group': supplies_group})


def all_write_offs(request):
    write_offs = Write_offs.objects.all()
    return render(request, 'write_offs.html', {'write_offs': write_offs})


def all_sales(request):
    sales = Sales.objects.all()
    total_cost = 0
    for sale in sales:
        total_cost += sale.cost
    return render(request, 'sales.html', {'sales': sales, 'total_cost': total_cost})
