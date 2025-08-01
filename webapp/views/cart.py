from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, FormView, TemplateView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Product


class CartAddView(FormView):
    form_class = CartForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        qty = form.cleaned_data["qty"]

        cart = self.request.session.get("cart", {})

        # {"1": 2, "3": 5}
        str_pk = str(product.pk)

        if str_pk in cart:
            full_qty = cart[str_pk] + qty
        else:
            full_qty = qty

        if full_qty > product.amount:
            errors = self.request.session.get("errors", {})
            errors[str_pk] = f"Количество продукта {product.title} на складе составляет {product.amount}"
            self.request.session["errors"] = errors
        else:
            cart[str_pk] = full_qty
            self.request.session['cart'] = cart
            self.request.session.pop("errors", {})

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        path = self.request.GET.get("path")
        if path:
            return path
        return reverse("webapp:index")


class CartView(TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, **kwargs):
        cart = self.request.session.get("cart", {})
        total = 0
        cart_list = []

        for product_pk, qty in cart.items():
            product = get_object_or_404(Product, pk=product_pk)
            total_price = product.price * qty

            cart_list.append({
                "qty": qty,
                "product": product,
                "total_price": total_price
            })
            total += total_price

        result = super().get_context_data(**kwargs)
        result['total'] = total
        result['cart_list'] = cart_list
        result['form'] = OrderForm(request=self.request)
        return result


class CartRemoveView(View):

    def get(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        cart = self.request.session.get("cart", {})
        if str(product.pk) in cart:
            cart.pop(str(product.pk))
        self.request.session['cart'] = cart
        return redirect("webapp:cart_view")


class CartOneProductRemoveView(View):

    def get(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        cart = self.request.session.get("cart", {})
        if str(product.pk) in cart:
            cart[str(product.pk)] -= 1
        if cart[str(product.pk)] == 0:
            cart.pop(str(product.pk))
        self.request.session['cart'] = cart
        return redirect("webapp:cart_view")

