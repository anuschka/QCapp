from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from qcapp.forms import ReagentForm, SearchForm
from django.template.response import TemplateResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView, UpdateView, DeleteView, FormMixin
from django.views.generic import ListView
from qcapp.models import Reagent


# @login_required
# def reagent_view(request):
#
#     # get all the Reagent objects
#     reagents = Reagent.objects.all()
#
#     # Sorting the Queryset
#     sort_by = request.GET.get('sortBy')
#     if sort_by == 'expiryDate':
#         reagents = reagents.order_by('expiry')
#     elif sort_by == 'entryDate':
#         reagents = reagents.order_by('created_at')
#     elif sort_by == 'lot':
#         reagents = reagents.order_by('lot')
#
#     # Using Paginator to split results accross serveral pages
#     paginator = Paginator(reagents, 2)  # Show 2 reagents per page
#     page = request.GET.get('page')
#     if page:
#         try:
#             reagents = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             reagents = paginator.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results
#             reagents = paginator.page(paginator.num_pages)
#     else:
#         reagents = paginator.page(1)
#
#     context = {
#         'reagents': reagents,
#         'active_page': 'reagent',
#         'paginator': paginator
#     }
#     return TemplateResponse(request, 'reagents.html', context)
class ReagentAllView(ListView):
    model = Reagent
    paginate_by = 4
    template_name = 'reagents.html'

    def get_context_data(self, **kwargs):
        context = super(ReagentAllView, self).get_context_data(**kwargs)
        context['active_page'] = 'reagent'
        reagent_list = Reagent.objects.all()
        paginator = Paginator(reagent_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            reagent_list = paginator.page(page)
        except PageNotAnInteger:
            reagent_list = paginator.page(1)
        except EmptyPage:
            reagent_list = paginator.page(paginator.num_pages)

        return context

    def get_queryset(self):
        queryset = Reagent.objects.all()
        sort_by = self.request.GET.get('sortBy')
        if sort_by == 'expiryDate':
            queryset = queryset.order_by('expiry')
        elif sort_by == 'entryDate':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'lot':
            queryset == queryset.order_by('lot')
        return queryset

reagent_view = login_required(ReagentAllView.as_view())

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


# @login_required
# def reagent_edit_view(request, id):
#
#     if request.method == 'GET':
#         print('edit', id)
#         obj = get_object_or_404(Reagent.objects.filter(id=id))
#         form = ReagentForm(instance=obj)
#         context = {
#             'active_page': 'reagent',
#             'id': id,
#             'form': form
#         }
#         return TemplateResponse(request, 'reagents_edit.html', context)
#     elif request.method == 'POST':
#         obj = get_object_or_404(Reagent.objects.filter(id=id))
#
#         form = ReagentForm(request.POST, instance=obj)
#         print(form.errors)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/reagent/')
#         context = {
#             'active_page': 'reagent',
#             'id': id,
#             'form': form
#         }
#         return TemplateResponse(request, 'reagents_edit.html', context)

class ReagentEditView(UpdateView):
    template_name = 'reagents_edit.html'
    form_class = ReagentForm

    def get_object(self, queryset=None):
        obj = Reagent.objects.get(id=self.args[0])
        return obj

#    def get_form(self, form_class):
#        """
#        Check if the user already saved reagent details. If so, then show
#        the form populated with those details, to let user change them.
#        """
#        try:
#            reagent = Reagent.objects.get(id=self.args[0])
#            return form_class(instance=reagent, **self.get_form_kwargs())
#        except Reagent.DoesNotExist:
#            return form_class(**self.get_form_kwargs())

#    def get_initial(self):
#        """
#        Use the get_initial method to prepoulate the form with data
#        """
#        super(ReagentEditView, self).get_initial()
#        reagent = Reagent.objects.get(id=self.args[0])
#        return self.reagent


    def get_context_data(self, **kwargs):
        context = super(ReagentEditView, self).get_context_data(**kwargs)
        context['active_page'] = 'reagent'
        return context

    def form_valid(self, form, **kwargs):
        form.save()
        return HttpResponseRedirect('/reagent/')

reagent_edit_view = login_required(ReagentEditView.as_view())


# @login_required
# @require_POST
# def delete_record_view(request, id):
#     obj = get_object_or_404(Reagent.objects.filter(id=id))
#     obj.delete()
#     return HttpResponseRedirect('/reagent/')

class DeleteReagentView(DeleteView):
    model = Reagent
    success_url = '/reagent/'

    def get_object(self, queryset=None):
        obj = Reagent.objects.get(id=self.args[0])
        return obj

delete_record_view = login_required(DeleteReagentView.as_view())

#@login_required
#def search_form_view(request):
#    if request.method == 'GET':
#        if 'keyword' in request.GET:
#            form = SearchForm(request.GET)
#            print(request)
#            print(form.errors)
#            if form.is_valid():
#                # if 'keyword' in request.POST and request.POST['keyword']:
#                q = form.cleaned_data['keyword']
#                print(q)
#                reagents_filtered = Reagent.objects.filter(
#                    Q(type__icontains=q) | Q(lot__icontains=q) |
#                    Q(manufacturer__icontains=q)
#                )
#                reagents = reagents_filtered
#                paginator = Paginator(reagents, 4)  # Show 4 reagents per page
#                page = request.GET.get('page')
#                GET_params = request.GET.copy()
#                if page:
#                    try:
#                        reagents = paginator.page(page)
#                    except PageNotAnInteger:
#                        # If page is not an integer, deliver first page.
#                        reagents = paginator.page(1)
#                    except EmptyPage:
#                        # If page is out of range (e.g. 9999), deliver last
#                        # page of results.
#                        reagents = paginator.page(paginator.num_pages)
#                else:
#                        reagents = paginator.page(1)
#                context = {
#                        'active_page': 'reagent',
#                        'form': form,
#                        'reagents': reagents,
#                        'reagents_filtered': reagents_filtered,
#                        'paginator': paginator,
#                        'GET_params': GET_params,
#                        'query': q
#                        }
#                return TemplateResponse(
#                    request, 'reagents_search.html', context)
#            else:
#                context = {
#                    'active_page': 'reagent',
#                    'form': form
#                }
#                return TemplateResponse(
#                    request, 'reagents_search.html', context)
#        form = SearchForm()
#        context = {
#            'active_page': 'reagent',
#            'form': form
#        }
#        return TemplateResponse(request, 'reagents_search.html', context)

class SearchReagentView(FormMixin, ListView):
    model = Reagent
    form_class = SearchForm
    template_name = 'reagents_search.html'
    queryset = Reagent.objects.all()
    paginate_by = 4

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            self.object_list = form.filter_queryset(request, self.object_list)

        context = self.get_context_data(form=form, object_list=self.object_list, active_page='reagent' ,query=self.request.GET.get('keyword'))

        return self.render_to_response(context)

#     def get_queryset(self):
#         form = self.form_class(self.request.GET)
#         if form.is_valid():
#             q = form.cleaned_data['keyword']
#             reagents_filtered = Reagent.objects.filter(
#                        Q(type__icontains=q) | Q(lot__icontains=q) |
#                        Q(manufacturer__icontains=q)
#                     )
#             paginator = Paginator(reagents_filtered, self.paginate_by)
#             page = self.request.GET.get('page')
#             try:
#                 reagent_list = paginator.page(page)
#             except PageNotAnInteger:
#                 reagent_list = paginator.page(1)
#             except EmptyPage:
#                 reagent_list = paginator.page(paginator.num_pages)
#             return reagent_list
#         return Reagent.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(SearchReagentView, self).get_context_data(**kwargs)
#         context['active_page'] = 'reagent'
#         return context

search_form_view = login_required(SearchReagentView.as_view())
