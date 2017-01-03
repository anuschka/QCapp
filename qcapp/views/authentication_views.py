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

#def login_view(request):
#    if request.user.is_authenticated():
#        # User is already logged in
#        return HttpResponseRedirect('/portal/')
#    if request.method == 'GET':
#        form = LoginForm()
#        return TemplateResponse(request, 'login.html', {'form': form})
#    elif request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            user = authenticate(username=username, password=password)
#            if user is None:
#                context = {
#                    'form': form,
#                    'error': 'No such user!'
#                }
#                return TemplateResponse(request, 'login.html', context)
#            if not user.is_active:
#                context = {
#                    'form': form,
#                    'error': 'Inactive user!'
#                }
#                return TemplateResponse(request, 'login.html', context)
#            login(request, user)
#            return HttpResponseRedirect('/portal/')
#        else:
#            return TemplateResponse(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated():
        # User is already logged in
        return HttpResponseRedirect('/portal/')
    if request.method == 'GET':
        form = RegistrationForm()
        return TemplateResponse(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if User.objects.filter(
             username=form.cleaned_data['username']).exists():
                # Username exists
                context = {
                    'form': form,
                    'error': 'Username exists!'
                }
                return TemplateResponse(request, 'register.html', context)

            if password1 != password2:
                # Password is not equal
                context = {
                    'form': form,
                    'error': 'Passwords do not match!'
                }
                return TemplateResponse(request, 'register.html', context)

            with transaction.atomic():
                user = User.objects.create_user(username, email, password1)
                profile = UserProfile.objects.create(user=user, roles='T')
            return HttpResponseRedirect('/portal/')
        else:
            return TemplateResponse(request, 'register.html', {'form': form})
