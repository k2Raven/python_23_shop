from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F


class Cart(models.Model):
    qty = models.PositiveIntegerField(default=1, verbose_name="Количество", validators=(MinValueValidator(1),))
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, verbose_name="Продукт")


    def get_total_price(self):
        return self.product.price * self.qty

    @classmethod
    def get_full_cart_price(cls):
        return cls.objects.aggregate(total=Sum(F('product__price') * F('qty')))['total'] or 0

        # total_price = 0
        # for cart in cls.objects.all():
        #     total_price += cart.get_total_price()
        # return total_price

    class Meta:
        db_table = "cart"
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"
