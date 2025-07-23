from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Product


class CartAddView(CreateView):
    model = Cart
    form_class = CartForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        qty = form.cleaned_data["qty"]

        try:
            cart = Cart.objects.get(product=product)
            full_qty = cart.qty + qty
        except Cart.DoesNotExist:
            full_qty = qty

        if full_qty > product.amount:
            return HttpResponseBadRequest(f"Количество продукта {product.title} на складе составляет {product.amount}")

        cart_product, _ = Cart.objects.get_or_create(product=product)
        cart_product.qty = full_qty
        cart_product.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        path = self.request.GET.get("path")
        if path:
            return path
        return reverse("webapp:index")


class CartView(ListView):
    model = Cart
    context_object_name = "cart_list"
    template_name = "cart/cart_view.html"

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['total'] = Cart.get_full_cart_price()
        result['form'] = OrderForm()
        return result


class CartRemoveView(DeleteView):
    model = Cart
    success_url = reverse_lazy("webapp:cart_view")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartOneProductRemoveView(DeleteView):
    model = Cart
    success_url = reverse_lazy("webapp:cart_view")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.qty == 1:
            return self.delete(request, *args, **kwargs)
        self.object.qty -= 1
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
