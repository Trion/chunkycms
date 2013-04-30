from django.test import TestCase, Client
from chunkycms.models import Page, SelfParent, Chunk
from django.contrib.auth.models import User


class SimpleTest(TestCase):

    fixtures = [
        "test/auth.json"
    ]

    def setUp(self):
        self.author = User.objects.get(email="test@example.com")
        self.client = Client()
        self.create_pages()

    def create_pages(self):
        """
        Creates a page with the slug test and a page with the slug foo and the other page as parent
        """
        test_page = Page()
        test_page.title = "Test"
        test_page.content = "This is just a Test"
        test_page.author = self.author
        test_page.save()

        foo_page = Page()
        foo_page.title = "Foo"
        foo_page.content = "Yet another Test"
        foo_page.author = self.author
        foo_page.parent = test_page
        foo_page.save()

    def test_page_model(self):
        """
        Tests Page Model
        """

        # Test page creation
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
        page = Page.get_by_path("test/foo")
        self.assertEqual(page.title, "Foo")

        # Test direct SelfParent Exception
        with self.assertRaises(SelfParent):
            page = Page.objects.get(slug="test")
            page.parent = page
            page.save()

        # Test chained SelfParent Exception
        with self.assertRaises(SelfParent):
            page = Page.objects.get(slug="test")
            page.parent = Page.get_by_path("test/foo")
            page.save()

    def test_page_availability(self):
        """
        Tests http status codes for pages
        """
        response = self.client.get("/test/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/test/foo/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/not-existent/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/not-existent/even-does-not-exist/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/test/not-existent/")
        self.assertEqual(response.status_code, 404)
