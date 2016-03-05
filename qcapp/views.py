from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

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
