from django.db.utils import IntegrityError
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.test import Client

from qcapp.models import Cell, CellPanel, UserProfile
from qcapp.views import index, login_view, portal_view, register_view


# Create your tests here.
class MyTest(TestCase):
    def test_our_view(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        # Create an instance of a GET request.
        request = self.factory.get('/portal/')

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #request.user = AnonymousUser # TODO
        #request.POST = {'username': "test", 'password': "test"}
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = portal_view(request)

        # Now, response is an object of type TemplateResponse

        response.context_data  #   --->
        assert len(response.context_data['cells']) == 0


        # Test the response status code here, verify it is a redirect
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_with_client(self):
        c = Client()

        # Issue a GET request for portal.
        response = c.get('/portal/')

        # Check that the response is 302.
        print(response, response.status_code, response.content)
        self.assertEqual(response.status_code, 302)


class ModelTest(TestCase):
    def test_cellpanel(self):
        CellPanel1 = CellPanel.objects.create(type='ID-DiaPanel 1', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel2 = CellPanel.objects.create(type='ID-DiaPanel 2', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel3 = CellPanel.objects.create(type='ID-DiaPanel 3', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel4 = CellPanel.objects.create(type='ID-DiaPanel 4', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel5 = CellPanel.objects.create(type='ID-DiaPanel 5', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel6 = CellPanel.objects.create(type='ID-DiaPanel 6', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')

        # Verify 6 object found.
        all_objects = CellPanel.objects.all()
        assert len(all_objects) == 6

        # Verify that the cell expiry date is correct.
        assert CellPanel1.expiry == "2016-03-14"

        # Test that an exception is raised when someone tries to enter one instance twice.
        with self.assertRaises(IntegrityError):
            CellPanel7 = CellPanel.objects.create(type='ID-DiaPanel 6', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')



    def test_cell(self):
        CellPanel1 = CellPanel.objects.create(type='ID-DiaPanel 1', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        cell1 = Cell.objects.create(cell_panel = CellPanel1, number= '1', type = 'Something', lot = 'Lot')

        cell1.save()
        assert len(Cell.objects.all()) == 1

class UserProfileTest(TestCase):
    def test_simple(self):
        user = User.objects.create_user('drwho', 'drwho@email.com', 'password')
        profile = UserProfile.objects.create(user=user, roles='A')



        # There should be one user in the db
        assert len(User.objects.all()) == 1

        # Find drwho
        drwho = User.objects.get(username='drwho')

        # Verify drwho is an admin
        assert profile.roles == 'A'

class ViewTest(TestCase):
    def test_validlogin(self):
        c=Client()

        # Test login view for valid username and password
        user = User.objects.create_user('drwho', 'drwho@email.com', 'password')
        profile = UserProfile.objects.create(user=user, roles='A')

        response = c.post('/login/', {'username': 'drwho', 'password': 'password'})
        print(response, response.status_code, response.content)
        self.assertEqual(response.status_code, 302)


    def test_register(self):
        c=Client()

        # Test register_view
        response = c.post('/register/', {'username': 'username', 'email': 'something@email.com', 'password1': 'passworditis', 'password2': 'passworditis'})
        print(response, response.status_code, response.content)
        self.assertEqual(response.status_code, 302)
        print ('Finished register new user test.')

    def test_portal(self):
        c=Client()
        # Test portal_view context data
        user = User.objects.create_user('drwho', 'drwho@email.com', 'password')
        profile = UserProfile.objects.create(user=user, roles='A')
        CellPanel1 = CellPanel.objects.create(type='ID-DiaPanel 1', manufacturer='DIA-MED', lot='06171.75.1', expiry='2016-03-14')
        CellPanel2 = CellPanel.objects.create(type='ID-DiaPanel 2', manufacturer='DIA-MED', lot='06171.75.2', expiry='2016-03-15')
        cell1 = Cell.objects.create(cell_panel = CellPanel1, number= '1', type = 'Something', lot = 'Lot')
        response = c.post('/login/', {'username': 'drwho', 'password': 'password'})
        response = c.get('/portal/')
        print(response, response.status_code, response.content)
        self.assertTrue(len(response.context_data['cells']) == 1)
        self.assertTrue(len(response.context_data['cell_panels']) == 2)
