from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.test import Client

from qcapp.models import SimpleItem
from qcapp.views import index


# Create your tests here.
class MyTest(TestCase):
    def test_item(self):
        # Verify 0 object found:
        all_objects = SimpleItem.objects.all()
        assert len(all_objects) == 0

        # Create a simple object (and save to dabase)
        my_object = SimpleItem.objects.create(name="My item")
        assert my_object.name == "My item"

        # Verify 1 object found:
        all_objects = SimpleItem.objects.all()
        assert len(all_objects) == 1

    def test_our_view(self):
        factory = RequestFactory()

        # Create an instance of a GET request.
        request = factory.get('/qcapp/')

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        print(response)

        # Test the response status code here, verify it is a redirect
        print(response.status_code)
        self.assertEqual(response.status_code, 302)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_with_client(self):
        # Issue a GET request. Making a GET request to the same directory as above /qcapp/
        response = self.client.get('/qcapp/')

        # Check that the response is 404 instead of 302 since the view /qcapp/ does not exist.
        self.assertEqual(response.status_code, 404)
