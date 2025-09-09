from django.test import TestCase
from http import HTTPStatus

from webapp.models import Product, Category
from webapp.tests.factories.category import CategoryFactory
from webapp.tests.factories.product import ProductFactory


class ProductViewTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory.create()

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


    def test_create_product_success(self):
        data = {
            "title": "Test Product",
            "description": "Test Description",
            "amount": 10,
            "price": 100.00,
            "category": self.category.id,
        }
        response = self.client.post('/products/add/', data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.title, data["title"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.amount, data["amount"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.category.id, data["category"])

    def test_create_product_fail(self):
        data = {
            "title": "",
            "description": "Test Description",
            "amount": -10,
            "price": -100.00,
            "category": "",
        }
        response = self.client.post('/products/add/', data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Product.objects.count(), 0)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'amount', 'Ensure this value is greater than or equal to 0.')
        self.assertFormError(response, 'form', 'price', 'Ensure this value is greater than or equal to 0.')
        self.assertFormError(response, 'form', 'category', 'This field is required.')


    def test_update_product_success(self):
        product = ProductFactory.create()
        data = {
            "title": "Test Product",
            "description": "Test Description",
            "amount": 10,
            "price": 100.00,
            "category": self.category.id,
        }
        response = self.client.post(f'/product/{product.pk}/update/', data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Product.objects.count(), 1)
        edit_product = Product.objects.first()
        self.assertEqual(edit_product.title, data["title"])
        self.assertEqual(edit_product.description, data["description"])
        self.assertEqual(edit_product.amount, data["amount"])
        self.assertEqual(edit_product.price, data["price"])
        self.assertEqual(edit_product.category.id, data["category"])

