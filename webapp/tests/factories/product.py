import factory
from factory.django import DjangoModelFactory

from webapp.tests.factories.category import CategoryFactory

from webapp.models import Product


class ProductFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Title {n}")
    description = factory.Sequence(lambda n: f"Description {n}")
    amount = factory.Faker("random_int", min=10, max=100)
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Product
