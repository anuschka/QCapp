from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
# from qcapp.models import UserProfile
from django.contrib.auth.models import User
from qcapp.forms import RegistrationForm, LoginForm, ReagentForm, SearchForm
from django.template.response import TemplateResponse
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import FormView


from qcapp.models import Cell, Reagent, IdCard, UserProfile, CellPanel


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

            with transaction.atomic():
                user = User.objects.create_user(username, email, password1)
                profile = UserProfile.objects.create(user=user, roles='T')
            return HttpResponseRedirect('/portal/')
        else:
            return TemplateResponse(request, 'register.html', {'form': form})

@login_required
def reagent_view(request):

    # get all the Reagent objects
    reagents = Reagent.objects.all()

    # http://localhost:8000/reagent/?sortBy=lot&page=8391
    # request.GET = {'sortBy':'lot', 'page':'8391'}

    sort_by = request.GET.get('sortBy')
    if sort_by == 'expiryDate':
        reagents = reagents.order_by('expiry')
    elif sort_by == 'entryDate':
        reagents = reagents.order_by('created_at')
    elif sort_by == 'lot':
        reagents = reagents.order_by('lot')

    paginator = Paginator(reagents, 2)  # Show 2 reagents per page
    page = request.GET.get('page')
    if page:
        try:
            reagents = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            reagents = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            reagents = paginator.page(paginator.num_pages)
    else:
        reagents = paginator.page(1)

    context = {
        #'reagents': reagents,
        'reagents': reagents,
        'active_page': 'reagent',
        'paginator': paginator
    }
    return TemplateResponse(request, 'reagents.html', context)

# @login_required
# def reagent_new_view(request):
#
#     if request.method == 'GET':
#         form = ReagentForm()
#         return TemplateResponse(request, 'reagents_new.html', {'form': form})
#     elif request.method == 'POST':
#         form = ReagentForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/reagent/')
#         context = {
#             'active_page': 'reagent',
#             'form': form
#         }
#         return TemplateResponse(request, 'reagents_new.html', context)


class ReagentNewView(FormView):
    template_name = 'reagents_new.html'
    form_class = ReagentForm

    def render_to_response(self, context):
        context['active_page'] = 'reagent'
        return super().render_to_response(context)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/reagent/')

reagent_new_view = ReagentNewView.as_view()


@login_required
def reagent_edit_view(request, id):

    if request.method == 'GET':
        print('edit', id)
        obj = get_object_or_404(Reagent.objects.filter(id=id))
        form = ReagentForm(instance=obj)
        context = {
            'active_page': 'reagent',
            'id': id,
            'form': form
        }
        return TemplateResponse(request, 'reagents_edit.html', context)
    elif request.method == 'POST':
        obj = get_object_or_404(Reagent.objects.filter(id=id))

        form = ReagentForm(request.POST, instance=obj)
        print(form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reagent/')
        context = {
            'active_page': 'reagent',
            'id': id,
            'form': form
        }
        return TemplateResponse(request, 'reagents_edit.html', context)


@login_required
def delete_record_view(request, id):
    obj = Reagent.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/reagent/')


@login_required
def search_form_view(request):
    if request.method == 'GET':
        form = SearchForm()
        context = {
            'active_page': 'reagent',
            'form': form
        }
        return TemplateResponse(request, 'reagents_search.html', context)
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            # if 'keyword' in request.POST and request.POST['keyword']:
            q = form.cleaned_data['keyword']
            reagents = Reagent.objects.filter(
                Q(type__icontains=q) | Q(lot__icontains=q)
                | Q(manufacturer__icontains=q)
            )
            context = {
                'active_page': 'reagent',
                'reagents': reagents,
                'query': q
                }
            return TemplateResponse(request, 'reagents_search.html', context)
        context = {
            'active_page': 'reagent',
            'form': form
        }
        return TemplateResponse(request, 'reagents_search.html', context)


@login_required
def search_view(request):
    if 'keyword' in request.GET:
        message = 'You searched for: %r' % request.GET['keyword']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
