from django.conf.urls import url
from qcapp.views import authentication_views
from qcapp.views import reagent_views
from qcapp.views import idcard_views
from qcapp.views import portal_views
from qcapp.views import cellpanel_views
from qcapp.views import cell_views
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
    url(
        r'^password_request/$', authentication_views.password_request_view,
        name='password_request_view'),
    url(
        r'^password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        authentication_views.password_confirm_view,
        name='password_confirm_view'),
    # Main portal.
    url(r'^portal/$', portal_views.portal_view, name='portal_page'),
    # Admin site.
    url(r'^admin/', admin.site.urls),
    # # # #  URLs for Reagent CRUD
    # Reagent view all and search.
    url(r'^reagent/$', reagent_views.reagent_view, name='reagent_view'),
    # Reagent add new record.
    url(r'^reagent/new/$', reagent_views.reagent_new_view,
        name='reagent_new_view'),
    # Reagent edit existing record..
    url(r'^reagent/([0-9]+)/edit/$', reagent_views.reagent_edit_view,
        name='reagent_edit_view'),
    # Reagent delete record.
    url(r'^reagent/([0-9]+)/delete/$', reagent_views.reagent_delete_record_view,
        name='reagent_delete_record_view'),
    # # # #  URLs for IdCard CRUD
    # IDCard view all and search.
    url(r'^idcard/$', idcard_views.idcard_view, name='idcard_view'),
    # IDCard add new record.
    url(r'^idcard/new/$', idcard_views.idcard_new_view,
        name='idcard_new_view'),
    # IDCard edit existing record.
    url(r'^idcard/([0-9]+)/edit/$', idcard_views.idcard_edit_view,
        name='idcard_edit_view'),
    # IDCard delete record.
    url(r'^idcard/([0-9]+)/delete/$', idcard_views.idcard_delete_record_view,
        name='idcard_delete_record_view'),
    # # # #  URLs for Cell Panel CRUD
    # Cell Panel view all and search.
    url(r'^cellpanel/$', cellpanel_views.cellpanel_view, name='cellpanel_view'),
    # Display all Cells for one Cell Panel.
    url(r'^cellpanel/([0-9]+)/$', cell_views.cell_view,
        name='cell_view'),
    # Add new Cell.
    url(r'^cellpanel/([0-9]+)/cell/new/$', cell_views.cell_new_view,
        name='cell_new_view'),
    # Cell inside the CellPanel.
    url(r'^cellpanel/([0-9]+)/cell/([0-9]+)/$', cell_views.cellpanel_cell_view,
        name='cellpanel_cell_view'),


]
