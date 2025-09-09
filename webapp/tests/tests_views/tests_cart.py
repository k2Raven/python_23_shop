from django.test import TestCase

from webapp.models import Product, Category, Cart
from webapp.tests.factories.category import CategoryFactory
from webapp.tests.factories.product import ProductFactory


class CartViewTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory.create(amount=3)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory.create()

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()

    def test_products_add_to_cart_view(self):
        self.assertIsNone(self.client.session.get('cart'))
        self.client.post(f'/product/{self.product.id}/add-cart/', {'qty': 1})
        self.assertIsNotNone(self.client.session.get('cart'))
        self.assertIsNone(self.client.session.get('errors'))
        self.assertDictEqual(self.client.session.get('cart'), {str(self.product.id): 1})

        self.client.post(f'/product/{self.product.id}/add-cart/', {'qty': 1})
        self.assertIsNotNone(self.client.session.get('cart'))
        self.assertIsNone(self.client.session.get('errors'))
        self.assertDictEqual(self.client.session.get('cart'), {str(self.product.id): 2})

        self.client.post(f'/product/{self.product.id}/add-cart/', {'qty': 1})
        self.assertIsNotNone(self.client.session.get('cart'))
        self.assertIsNone(self.client.session.get('errors'))
        self.assertDictEqual(self.client.session.get('cart'), {str(self.product.id): 3})

        self.client.post(f'/product/{self.product.id}/add-cart/', {'qty': 1})
        self.assertIsNotNone(self.client.session.get('cart'))
        self.assertDictEqual(self.client.session.get('cart'), {str(self.product.id): 3})
        self.assertIsNotNone(self.client.session.get('errors'))
        self.assertDictEqual(self.client.session.get('errors'), {
            str(self.product.id): f'Количество продукта {self.product.title} на складе составляет {self.product.amount}'})
