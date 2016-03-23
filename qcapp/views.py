from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import auth
from django.core.context_processors import csrf
from qcapp.models import UserProfile
from qcapp.forms import RegistrationForm
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404

@login_required
def index(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return render_to_response('qcapp/index.html')

def logout_page(request):
    """Log users out and re-direct them to the main page."""
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('register.html', {'has_account': True})
    manipulator = RegistrationForm()
    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            # Save the user
            manipulator.do_html2python(new_data)
            new_user = manipulator.save(new_data)

            # Build the activation key for their account
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Create and save their profile
            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            return render_to_response('register.html', {'created': True})
    else:
        errors = new_data = {}
    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('register.html', {'form': form})
