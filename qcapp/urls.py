from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Login / logout.
    url(r'^login/$', login),
    url(r'^logout/$', views.logout_page, name='logout_page'),
]
