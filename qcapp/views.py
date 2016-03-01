from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return render_to_response('qcapp/index.html')
