from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from qcapp.forms import ReagentForm, SearchForm
from django.template.response import TemplateResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from qcapp.models import Reagent


@login_required
def reagent_view(request):

    # get all the Reagent objects
    reagents = Reagent.objects.all()

    # Sorting the Queryset
    sort_by = request.GET.get('sortBy')
    if sort_by == 'expiryDate':
        reagents = reagents.order_by('expiry')
    elif sort_by == 'entryDate':
        reagents = reagents.order_by('created_at')
    elif sort_by == 'lot':
        reagents = reagents.order_by('lot')

    # Using Paginator to split results accross serveral pages
    paginator = Paginator(reagents, 2)  # Show 2 reagents per page
    page = request.GET.get('page')
    if page:
        try:
            reagents = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            reagents = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            reagents = paginator.page(paginator.num_pages)
    else:
        reagents = paginator.page(1)

    context = {
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

# Class based view for New reagent
class ReagentNewView(FormView):
    template_name = 'reagents_new.html'
    form_class = ReagentForm

    def render_to_response(self, context):
        context['active_page'] = 'reagent'
        return super().render_to_response(context)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/reagent/')

reagent_new_view = login_required(ReagentNewView.as_view())


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
@require_POST
def delete_record_view(request, id):
    obj = Reagent.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/reagent/')


@login_required
def search_form_view(request):
    if request.method == 'GET':
        if 'keyword' in request.GET:
            form = SearchForm(request.GET)
            print(request)
            print(form.errors)
            if form.is_valid():
                # if 'keyword' in request.POST and request.POST['keyword']:
                q = form.cleaned_data['keyword']
                print(q)
                reagents_filtered = Reagent.objects.filter(
                    Q(type__icontains=q) | Q(lot__icontains=q) |
                    Q(manufacturer__icontains=q)
                )
                reagents = reagents_filtered
                paginator = Paginator(reagents, 4)  # Show 4 reagents per page
                page = request.GET.get('page')
                GET_params = request.GET.copy()
                if page:
                    try:
                        reagents = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        reagents = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last
                        # page of results.
                        reagents = paginator.page(paginator.num_pages)
                else:
                        reagents = paginator.page(1)
                context = {
                        'active_page': 'reagent',
                        'form': form,
                        'reagents': reagents,
                        'reagents_filtered': reagents_filtered,
                        'paginator': paginator,
                        'GET_params': GET_params,
                        'query': q
                        }
                return TemplateResponse(
                    request, 'reagents_search.html', context)
            else:
                context = {
                    'active_page': 'reagent',
                    'form': form
                }
                return TemplateResponse(
                    request, 'reagents_search.html', context)
        form = SearchForm()
        context = {
            'active_page': 'reagent',
            'form': form
        }
        return TemplateResponse(request, 'reagents_search.html', context)
