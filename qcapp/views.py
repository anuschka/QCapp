from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
# from qcapp.models import UserProfile
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm
from django.template.response import TemplateResponse
# import datetime


@login_required
def index(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return TemplateResponse(request, 'qcapp/index.html', {})


def logout_page(request):
    """Log users out and re-direct them to the main page."""
    logout(request)
    return HttpResponseRedirect('/')


def login_page(request):
    context = {}
    form = LoginForm()
    context['form'] = form

    return TemplateResponse(request, 'registration/login.html', context)


def auth_page(request):
    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return TemplateResponse(request, 'qcapp/index.html', {'user': request.user})
        else:
            # Return a 'disabled account' error message
            context = {}
            form = LoginForm()
            context['form'] = form

            return TemplateResponse(request, 'registration/disabled.html', context)
    else:
        # Return an 'invalid login' error message.
        context = {}
        form = RegistrationForm()
        context['form'] = form

        return TemplateResponse(request, 'registration/invalid.html', context)

def portal_page(request):
    return TemplateResponse(request, 'qcapp/index.html', {'user': request.user})


def register_page(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        user = User.objects.create_user(username, email, password)

        return HttpResponseRedirect('/portal/')
    else:
        return HttpResponseRedirect('/login/')


def register(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('register.html', {'has_account': True})
    form = RegistrationForm()
    if request.POST:
        new_data = request.POST.copy()
        errors = form.get_validation_errors(new_data)
        if not errors:

            # # Create and save their profile
            # new_profile = UserProfile(user=new_user,
            #                           activation_key=activation_key,
            #                           key_expires=key_expires)
            # new_profile.save()

            return render_to_response('register.html', {'created': True})
    else:
        errors = new_data = {}
    return render_to_response('register.html', {'form': form})
