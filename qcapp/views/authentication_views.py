from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm
from django.template.response import TemplateResponse
from django.db import transaction
from qcapp.models import UserProfile
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from qcapp.forms import PasswordResetRequestForm, SetPasswordForm
from django.db.models.query_utils import Q
from mysite.settings import DEFAULT_FROM_EMAIL


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
            user = authenticate(username=username, password=password1)
            login(self.request, user)
            messages.success(
                self.request, 'You registered successfully!')
        return HttpResponseRedirect('/portal/')
register_view = RegisterView.as_view()


class PasswordRequestView(FormView):
    # code for template is given below the view's code
    template_name = "password_request.html"
    success_url = '/login/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'password_reset_subject.txt'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_subject.txt
        # to templates directory
        email_template_name = 'password_reset_email.html'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_email.html
        # to templates directory
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)
        print(subject)
        print(email)

    def form_valid(self, form):
        data = form.cleaned_data["email_or_username"]
        # uses the method written above
        if self.validate_email_address(data) is True:
            '''
            If the input is an valid email address, then the following code
            will lookup for users associated with that email address. If found
            then an email will be sent to the address, else an error message
            will be printed on the screen.
            '''
            associated_users = User.objects.filter(
                Q(email=data) | Q(username=data))
            print('assoc', list(associated_users))
            if associated_users.exists():
                for user in associated_users:
                    self.reset_password(user, self.request)
                messages.success(
                    self.request, 'An email has been sent to {0}. Please check its inbox to continue reseting password.'.format(data))
                return HttpResponseRedirect('/login/')
            else:
                result = self.form_invalid(form)
                messages.warning(
                    self.request, 'No user is associated with this email address')
                return result
        else:
            '''
            If the input is an username, then the following code will lookup
            for users associated with tportal/hat user. If found then an email will be
            sent to the user's address, else an error message will be printed
            on the screen.
            '''
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    self.reset_password(user, self.request)
                messages.success(
                    self.request, "Email has been sent to {0}'s email address. Please check its inbox to continue reseting password.".format(data))
                return HttpResponseRedirect('/login/')
            else:
                result = self.form_invalid(form)
                messages.warning(
                    self.request, 'This username does not exist in the system.')
                return result
                print(data)
        messages.warning(self.request, 'Invalid Input')
        return self.form_invalid(form)

password_request_view = PasswordRequestView.as_view()


class PasswordConfirmView(FormView):
    template_name = "password_confirm.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def form_valid(self, form):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']

        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 != password2:
            form.add_error(None, 'Passwords do not match!')
            return self.form_invalid(form)
        else:
            uid = urlsafe_base64_decode(uidb64)
            try:
                user = User.objects.get(pk=uid)
            except user.DoesNotExist:
                form.add_error(None, 'Invalid token')
                return self.form_invalid(form)

            if not default_token_generator.check_token(user, token):
                form.add_error(None, 'Invalid token')
                return self.form_invalid(form)

            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
            messages.success(self.request, 'Password has been reset.')
            return super().form_valid(form)


password_confirm_view = PasswordConfirmView.as_view()
