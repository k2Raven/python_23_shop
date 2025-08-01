from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import Order, Cart, OrderProduct, Product


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors["__all__"])

    def form_valid(self, form):
        with transaction.atomic():
            order = form.save()
            products = []
            order_products = []

            cart = self.request.session.get("cart", {})

            for product_id, qty in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                order_products.append(OrderProduct(order=order, product=product, qty=qty))
                product.amount -= qty
                products.append(product)

            OrderProduct.objects.bulk_create(order_products)
            Product.objects.bulk_update(products, ["amount"])
            self.request.session.pop("cart", {})

            return redirect("webapp:index")