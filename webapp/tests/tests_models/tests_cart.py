from django.test import TestCase

from webapp.models import Product, Category, Cart
from webapp.tests.factories.category import CategoryFactory
from webapp.tests.factories.product import ProductFactory


class CartModelTestCase(TestCase):
    def setUp(self):
        # product_1 = Product.objects.create(
        #     title="Test Product 1",
        #     description="Test Description 1",
        #     amount=10,
        #     price=100.00,
        #     category=self.category,
        # )
        # product_2 = Product.objects.create(
        #     title="Test Product 2",
        #     description="Test Description 2",
        #     amount=10,
        #     price=200.00,
        #     category=self.category,
        # )
        # product_3 = Product.objects.create(
        #     title="Test Product 3",
        #     description="Test Description 3",
        #     amount=10,
        #     price=300.00,
        #     category=self.category,
        # )
        # self.products = [product_1, product_2, product_3]
        self.products = [
            ProductFactory.create(price=100),
            ProductFactory.create(price=200),
            ProductFactory.create(price=300),
        ]

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory.create()

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


    def test_get_full_cart_price(self):
        for product in self.products:
            Cart.objects.create(product=product, qty=2)
        result = Cart.get_full_cart_price()
        self.assertEqual(result, 1200)