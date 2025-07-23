from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import Order, Cart, OrderProduct, Product


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    # def form_valid(self, form):
    #
    #     with transaction.atomic():
    #         order = form.save()
    #
    #         for item in Cart.objects.all():
    #             OrderProduct.objects.create(order=order, product=item.product, qty=item.qty)
    #             item.product.amount -= item.qty
    #             item.product.save()
    #             item.delete()
    #
    #         return redirect("webapp:index")

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors["__all__"])

    def form_valid(self, form):
        with transaction.atomic():
            order = form.save()
            products = []
            order_products = []

            for item in Cart.objects.all():
                order_products.append(OrderProduct(order=order, product=item.product, qty=item.qty))
                item.product.amount -= item.qty
                products.append(item.product)

            OrderProduct.objects.bulk_create(order_products)
            Product.objects.bulk_update(products, ["amount"])
            Cart.objects.all().delete()

            return redirect("webapp:index")