from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
# from qcapp.models import UserProfile
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm
from django.template.response import TemplateResponse
# import datetime

from qcapp.models import Cell, Reagent, IDcard


@login_required
def index(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return TemplateResponse(request, 'index.html', {})


def logout_view(request):
    """Log users out and re-direct them to the main page."""
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.user.is_authenticated():
        # User is already logged in
        return HttpResponseRedirect('/portal/')
    if request.method == 'GET':
        form = LoginForm()
        return TemplateResponse(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                context = {
                    'form': form,
                    'error': 'No such user!'
                }
                return TemplateResponse(request, 'login.html', context)
            if not user.is_active:
                context = {
                    'form': form,
                    'error': 'Inactive user!'
                }
                return TemplateResponse(request, 'login.html', context)
            login(request, user)
            return HttpResponseRedirect('/portal/')
        else:
            return TemplateResponse(request, 'login.html', {'form': form})


@login_required
def portal_view(request):
    cells = Cell.objects.all()
    reagents = Reagent.objects.all()
    idcards = IDcard.objects.all()
    context = {
        'user': request.user,
        'cells': cells,
        'reagents': reagents,
        'idcards': idcards
    }
    return TemplateResponse(request, 'portal.html', context)


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

            if User.objects.filter(username=form.cleaned_data['username']).exists():
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

            with transaction.atomic(): # TODO
                user = User.objects.create_user(username, email, password1)
                profile = Profile.objects.create(...) # TODO
            return HttpResponseRedirect('/portal/')
        else:
            return TemplateResponse(request, 'register.html', {'form': form})
