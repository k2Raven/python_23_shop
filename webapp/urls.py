from django.urls import path

from webapp.views import ProductListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView
from webapp.views.cart import CartAddView, CartView, CartRemoveView, CartOneProductRemoveView
from webapp.views.orders import OrderCreateView

app_name = "webapp"

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('products/add/', ProductCreateView.as_view(), name="product_add"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),

    path('product/<int:pk>/add-cart/', CartAddView.as_view(), name="product_add_cart"),

    path('product/<int:pk>/remove-cart/', CartRemoveView.as_view(), name="product_remove_cart"),

    path('product/<int:pk>/remove-one-cart/', CartOneProductRemoveView.as_view(), name="product_one_remove_cart"),
    path('cart/', CartView.as_view(), name="cart_view"),

    path('create-order/', OrderCreateView.as_view(), name="order_create_view"),

]
