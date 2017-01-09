from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm
from django.template.response import TemplateResponse
from django.db import transaction
from qcapp.models import UserProfile
from django.views.generic.edit import FormView


def logout_view(request):
    # Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    # Main first page for the app.
    return TemplateResponse(request, 'index.html')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password'],
            any_account=True
            )
        if user is None:
            form.add_error(None, 'Invalid email/password')
            return self.form_invalid(form)
        if not user.is_active:
            form.add_error(
                None, 'Your account has been disabled, please contact us.'
                )
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect('/portal/')
login_view = LoginView.as_view()


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        data = form.cleaned_data
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if User.objects.filter(username=data['username']).exists():
            form.add_error(None, 'Username exists!')
            return self.form_invalid(form)
        if password1 != password2:
            form.add_error(None, 'Passwords do not match!')
            return self.form_invalid(form)

        with transaction.atomic():
            user = User.objects.create_user(username, email, password1)
            profile = UserProfile.objects.create(user=user, roles='T')
        return HttpResponseRedirect('/portal/')
register_view = RegisterView.as_view()
