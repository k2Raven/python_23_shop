from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Order(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Имя")
    phone = models.CharField(max_length=50, null=False, blank=False, verbose_name="Телефон")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    create_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    products = models.ManyToManyField(
        'webapp.Product',
        related_name="orders",
        through="webapp.OrderProduct",
        through_fields=('order', 'product'))

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(models.Model):
    order = models.ForeignKey("webapp.Order", on_delete=models.RESTRICT, verbose_name="Заказ")
    product = models.ForeignKey("webapp.Product", on_delete=models.RESTRICT, verbose_name="Продукт")
    qty = models.PositiveIntegerField(default=1, verbose_name="Количество", validators=(MinValueValidator(1),))

    class Meta:
        db_table = "orders_products"
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказов"
