from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Login / logout.
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    # Register new users.
    url(r'^register/$', views.register_view, name='register_view'),
    # Main portal.
    url(r'^portal/$', views.portal_view, name='portal_page'),
    # Admin site.
    url(r'^admin/', admin.site.urls),
    # Reagent All site.
    url(r'^reagent/$', views.reagent_view, name='reagent_view'),
    # Reagent add new.
    url(r'^reagent/new/$', views.reagent_new_view, name='reagent_new_view'),
    # Reagent add new.
    url(r'^reagent/([0-9]+)/edit/$', views.reagent_edit_view, name='edit-reagent'),
]
