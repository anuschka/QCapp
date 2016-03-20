from django.db.utils import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.test import Client

from qcapp.models import Cell
from qcapp.views import index


# Create your tests here.
class MyTest(TestCase):
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


class ModelTest(TestCase):
    def test_cell(self):
        cell1 = Cell.objects.create(number=1, type='ID-DiaPanel 1', lot='06171.75.1', expiry='2016-03-14')
        cell2 = Cell.objects.create(number=2, type='ID-DiaPanel 2', lot='06171.75.1', expiry='2016-03-14')
        cell3 = Cell.objects.create(number=3, type='ID-DiaPanel 3', lot='06171.75.1', expiry='2016-03-14')
        cell4 = Cell.objects.create(number=4, type='ID-DiaPanel 4', lot='06171.75.1', expiry='2016-03-14')
        cell5 = Cell.objects.create(number=5, type='ID-DiaPanel 5', lot='06171.75.1', expiry='2016-03-14')
        cell6 = Cell.objects.create(number=6, type='ID-DiaPanel 6', lot='06171.75.1', expiry='2016-03-14')

        # Verify 6 object found.
        all_objects = Cell.objects.all()
        assert len(all_objects) == 6

        # Verify that the cell expiry date is correct > this test raises an error / I believe it shouldn't
        assert cell1.expiry == "2016-03-14"

        # Test that an exception is raised when someone tries to enter one instance twice.
        with self.assertRaises(IntegrityError):
            cell7 = Cell.objects.create(number=4, type='ID-DiaPanel 3', lot='06171.75.1')

    def test_cell2(self):
        cell1 = Cell.objects.create(number=1, type='Something', lot='Lot')

        cell2 = Cell.objects.create(number=3, type='Something2', lot='Lot')
        cell2.type = 'Something'

        with self.assertRaises(IntegrityError):
            cell2.save()


def ProfileTest(TestCase):
    def test_simple(self):
        user = User.objects.create_user('drwho', 'drwho@email.com', 'password')
        profile = Profile.objects.create(user=user, role='A')

        # There should be one user in the db
        assert len(User.objects.all()) == 1

        # Find drwho
        drwho = User.objects.get(username='drwho')

        # Verify drwho is an admin
        assert drwho.profile.role == 'A'
