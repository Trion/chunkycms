from django.test import TestCase
from chunkycms.models import Page, SelfParent
from django.contrib.auth.models import User


class SimpleTest(TestCase):

    fixtures = [
        "test/auth.json"
    ]

    def setUp(self):
        self.author = User.objects.get(email="test@example.com")

    def test_page_model(self):
        """
        Tests Page Model
        """

        # Test page creation
        page = Page()
        page.title = "Test"
        page.content = "This is just a Test"
        page.author = self.author
        page.save()

        page = Page.objects.get(slug="test")
        self.assertEqual(page.title, "Test")

        # Test automatic slug generation
        page = Page()
        page.title = "Test"
        page.content = "Yet another Test"
        page.author = self.author
        page.save()
        page = Page.objects.get(slug="test1")
        self.assertEqual(page.content, "Yet another Test")

        # Test get by path
        pk = page.pk
        page.parent = Page.objects.get(slug="test")
        page.save()
        page = Page.get_by_path("test/test1")
        self.assertEqual(page.pk, pk)

        # Test direct SelfParent Exception
        with self.assertRaises(SelfParent):
            page = Page.objects.get(slug="test")
            page.parent = page
            page.save()

        # Test chained SelfParent Exception
        with self.assertRaises(SelfParent):
            page = Page.objects.get(slug="test")
            page.parent = Page.get_by_path("test/test1")
            page.save()
