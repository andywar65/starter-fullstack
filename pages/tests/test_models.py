from django.test import TestCase, override_settings

from pages.models import Article, HomePage


@override_settings(USE_I18N=False)
class PageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest page models")
        # Set up non-modified objects used by all test methods
        HomePage.objects.create(title="Title")
        HomePage.objects.create(intro="No title")
        Article.objects.create(title="First", date="2022-04-09")
        Article.objects.create(title="Central", date="2022-04-10")
        Article.objects.create(title="Last", date="2022-04-11")

    def test_homepage_str(self):
        hp1 = HomePage.objects.get(title="Title")
        self.assertEquals(hp1.__str__(), "Title")
        hp2 = HomePage.objects.get(intro="No title")
        self.assertEquals(hp2.__str__(), "Home Page - " + str(hp2.id))
        print("\n-Test Homepage titles")

    def test_article_names(self):
        a = Article.objects.get(title="First")
        self.assertEquals(a.__str__(), "First")
        print("\n-Test Article title")
        self.assertEquals(a.slug, "first")
        print("\n-Test Article slug")

    def test_article_get_path(self):
        a = Article.objects.get(title="First")
        self.assertEquals(a.get_path(), "/en/articles/2022/4/9/first/")
        print("\n-Test Article path")

    def test_article_previous_next(self):
        first = Article.objects.get(title="First")
        central = Article.objects.get(title="Central")
        last = Article.objects.get(title="Last")
        self.assertEquals(central.get_previous(), first)
        self.assertEquals(central.get_next(), last)
        self.assertEquals(first.get_previous(), None)
        self.assertEquals(last.get_next(), None)
        print("\n-Test previous and next Article")
