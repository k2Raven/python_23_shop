from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Product, Cart, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CartForm(forms.Form):
    qty = forms.IntegerField(min_value=1, max_value=100)

    class Meta:
        fields = ("qty",)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name", "phone", "address")


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        cart = self.request.session.get("cart", {})
        if not cart:
            raise ValidationError("Не выбрано ни одного товара")
        for product_pk, qty in cart.items():
            try:
                product = Product.objects.get(pk=product_pk)
                if qty > product.amount:
                    if product.amount:
                        raise ValidationError(f'Товара {product.title} оасталось {product.amount}')
                    raise ValidationError(f'Товар {product.title} закончился')
            except Product.DoesNotExist:
                raise ValidationError("Один из товаров удален")
        return data
