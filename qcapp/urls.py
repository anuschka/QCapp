from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Login / logout.
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^portal/$', views.portal_page, name='portal_page'),
    # Admin site.
    url(r'^admin/', admin.site.urls),
]
