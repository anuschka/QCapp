from django.conf.urls import url
from qcapp.views import authentication_views
from qcapp.views import reagent_views
from qcapp.views import portal_views
from django.contrib import admin

urlpatterns = [
    url(r'^$', authentication_views.index, name='index'),
    # Login / logout.
    url(r'^login/$', authentication_views.login_view, name='login_view'),
    url(r'^logout/$', authentication_views.logout_view, name='logout_view'),
    # Register new users.
    url(
        r'^register/$', authentication_views.register_view,
        name='register_view'),
    # Main portal.
    url(r'^portal/$', portal_views.portal_view, name='portal_page'),
    # Admin site.
    url(r'^admin/', admin.site.urls),
    # Reagent All site.
    url(r'^reagent/$', reagent_views.reagent_view, name='reagent_view'),
    # Reagent add new.
    url(r'^reagent/new/$', reagent_views.reagent_new_view,
        name='reagent_new_view'),
    # Reagent add new.
    url(r'^reagent/([0-9]+)/edit/$', reagent_views.reagent_edit_view,
        name='reagent_edit_view'),
    # Reagent delete record.
    url(r'^reagent/([0-9]+)/delete/$', reagent_views.delete_record_view,
        name='delete_record_view'),
    # Reagent serach form.
    url(r'^reagent/search-form/$', reagent_views.search_form_view,
        name='search_form_view'),
    url(
        r'^password_request/$', authentication_views.password_request_view,
        name='password_request_view'),
    url(
        r'^password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        authentication_views.password_confirm_view, name='password_confirm_view'),
]
