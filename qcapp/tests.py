from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

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

        # TODO: Test the response status code here, verify it is a redirect
        # ...
