import factory
from factory.django import DjangoModelFactory

from webapp.models import Category


class CategoryFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Category {n}")

    class Meta:
        model = Category
