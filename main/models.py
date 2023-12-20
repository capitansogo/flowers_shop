import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# роли
class Roles(models.Model):
    name = models.CharField(max_length=50, verbose_name='Роль', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


# филиалы
class Filials(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=50, verbose_name='Дом', blank=True, null=True)
    email = models.CharField(max_length=50, verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True, null=True)

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


# пользователи
class Users(AbstractUser):
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, verbose_name='Роль', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.role}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# услуги
class Services(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', blank=True, null=True)
    cost = models.CharField(max_length=50, verbose_name='Стоимость', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


# заказы на услуги
class Service_order(models.Model):
    client = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Клиент', blank=True, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Услуга', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)
    registration_date = models.DateField(verbose_name='Дата заявки', blank=True, null=True)
    date_completion = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    cost = models.FloatField(verbose_name='Стоимость', blank=True, null=True)

    def __str__(self):
        return f'{self.client} {self.service}'

    class Meta:
        verbose_name = 'Заказ на услугу'
        verbose_name_plural = 'Заказы на услуги'


# типы товаров
class Types_products(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'


# товары
class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', blank=True, null=True)
    type_product = models.ForeignKey(Types_products, on_delete=models.CASCADE, verbose_name='Тип продукта', blank=True,
                                     null=True)
    cost = models.FloatField(verbose_name='Стоимость', blank=True, null=True)
    photo = models.ImageField(upload_to='products', verbose_name='Фото', blank=True, null=True)
    stock_balance = models.IntegerField(verbose_name='Остаток на складе', blank=True, null=True)
    sheif_life = models.IntegerField(verbose_name='Срок годности', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# заказы
class Product_order(models.Model):
    client = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Клиент', blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)
    registration_date = models.DateField(verbose_name='Дата заявки', blank=True, null=True)
    date_completion = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    cost = models.FloatField(verbose_name='Стоимость', blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Количество', blank=True, null=True)

    def __str__(self):
        return f'{self.client} {self.product} {self.quantity}'

    # при сохранении дата выполнения равна дата заявка + 3 дня
    def save(self, *args, **kwargs):
        self.date_completion = self.registration_date + datetime.timedelta(days=3)

        # создание записи в таблице продаж
        sale = Sales()
        sale.product = self.product
        sale.filial = self.filial
        sale.date = self.date_completion
        sale.cost = self.cost
        sale.save()

        write_offs = Write_offs()
        write_offs.product = self.product
        write_offs.filial = self.filial
        write_offs.date = self.date_completion
        write_offs.quantity = self.quantity
        write_offs.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ на товар'
        verbose_name_plural = 'Заказы на товары'



# продажи
class Sales(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    cost = models.FloatField(verbose_name='Стоимость', blank=True, null=True)

    def __str__(self):
        return f'{self.product} {self.filial} {self.date} {self.cost}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'


# списания
class Write_offs(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Количество', blank=True, null=True)

    def __str__(self):
        return f'{self.product} {self.filial} {self.date} {self.quantity}'

    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'


# поставки
class Supplies(models.Model):
    delivery_date = models.DateField()
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name='Филиал', blank=True, null=True)

    def __str__(self):
        return f'{self.filial} {self.delivery_date}'

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'


# поставки товаров
class SuppliesItems(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    supplies = models.ForeignKey(Supplies, on_delete=models.CASCADE, verbose_name='Поставка', blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Количество', blank=True, null=True)

    def __str__(self):
        return f'{self.product} {self.supplies} {self.quantity}'

    class Meta:
        verbose_name = 'Поставка товара'
        verbose_name_plural = 'Поставки товаров'
