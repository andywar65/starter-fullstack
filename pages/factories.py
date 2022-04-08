from factory import Faker  # , SubFactory
from factory.django import DjangoModelFactory

from .models import Article


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = Faker("sentence", nb_words=3)
    intro = Faker("sentence", nb_words=5)
    body = Faker("sentence", nb_words=20)
