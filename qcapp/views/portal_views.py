from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm
from django.template.response import TemplateResponse
from django.db import transaction
from qcapp.models import Cell, UserProfile, CellPanel


@login_required
def index(request):
    # If users are authenticated, direct them to the main page. Otherwise, take
    # them to the login page.
    return TemplateResponse(request, 'index.html', {})


@login_required
def portal_view(request):

    # get all the CellPanel objects
    cellpanels = CellPanel.objects.all()

    # get all the Cell objects
    cells = Cell.objects.filter(cell_panel__manufacturer__contains='DIA-MED')

    # get all the Reagent objects
    ## get all the idcard objects
    #reagents = Reagent.objects.all()
    #idcards = IdCard.objects.all()

    # get all the CellPanel objects for Cell=cell1
    #cell1 = Cell.objects.filter(number=1)
    #cellpanels1 = CellPanel.objects.filter(cell=cell1)
    # get all the CellPanel objects using lists
    #cellpanel_list = []
    #for cell in cells:
    #    cellpanels = CellPanel.objects.filter(cell=cell)
    #    cellpanel_list += cellpanels
    # get all the CellPanel objects using dictionaries
    #cell_cellpanel_map = {}
    #for cell in cells:
#        l = []
#        for cellpanel in cellpanels:
#            if cellpanel.cell == cell:
#                l.append(cellpanel)
#        cell_cellpanel_map[cell] = l
    context = {
        'user': request.user,
        'cell_panels': cellpanels,
        'cells': cells,
#         'reagents': reagents,
#         'idcards': idcards,
#         'cellpanels1': cellpanels1,
#         'cellpanel_list': cellpanel_list,
#         'cell_cellpanel_map': cell_cellpanel_map
    }
    return TemplateResponse(request, 'portal.html', context)
