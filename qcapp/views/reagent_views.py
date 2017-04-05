from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from qcapp.forms import ReagentForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from qcapp.models import Reagent
from django.contrib import messages
from django.template.response import TemplateResponse


class ReagentAllView(ListView):
    model = Reagent
    paginate_by = 4
    template_name = 'reagents.html'

    def get_context_data(self, **kwargs):
        context = super(ReagentAllView, self).get_context_data(**kwargs)
        context['active_page'] = 'reagent'
        return context

    def get_queryset(self):
        queryset = Reagent.objects.all()

        if 'keyword' in self.request.GET:
            q = self.request.GET['keyword']
            if q:
                queryset = queryset.filter(
                    Q(type__icontains=q) | Q(lot__icontains=q) |
                    Q(manufacturer__icontains=q)
                )

        sort_by = self.request.GET.get('sortBy')
        if sort_by == 'expiryDate':
            queryset = queryset.order_by('expiry')
        elif sort_by == 'entryDate':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'lot':
            queryset == queryset.order_by('lot')
        return queryset

reagent_view = login_required(ReagentAllView.as_view())


class ReagentNewView(FormView):
    template_name = 'reagents_new.html'
    form_class = ReagentForm

    def render_to_response(self, context):
        context['active_page'] = 'reagent'
        return super().render_to_response(context)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, 'You entered a new reagent successfully!')
        return HttpResponseRedirect('/reagent/')

reagent_new_view = login_required(ReagentNewView.as_view())


class ReagentEditView(UpdateView):
    template_name = 'reagents_edit.html'
    form_class = ReagentForm

    def get_object(self, queryset=None):
        obj = Reagent.objects.get(id=self.args[0])
        return obj

    def get_context_data(self, **kwargs):
        context = super(ReagentEditView, self).get_context_data(**kwargs)
        context['active_page'] = 'reagent'
        return context

    def form_valid(self, form, **kwargs):
        form.save()
        messages.success(
            self.request, 'You changed the reagent successfully!')
        return HttpResponseRedirect('/reagent/')

reagent_edit_view = login_required(ReagentEditView.as_view())


class DeleteReagentView(DeleteView):
    model = Reagent
    success_url = '/reagent/'

    def get_object(self, queryset=None):
        obj = Reagent.objects.get(id=self.args[0])
        messages.success(
            self.request, 'You deleted the reagent successfully!')
        return obj

delete_record_view = login_required(DeleteReagentView.as_view())


def reagent_views(request):
    queryset = Reagent.objects.all()
    if 'keyword' in request.GET.get:
        q = request.GET.get['keyword']
        if q:
            queryset = queryset.filter(
                    Q(type__icontains=q) | Q(lot__icontains=q) |
                    Q(manufacturer__icontains=q)
            )
        context = {
            'active_page': 'reagent',
            'queryset': queryset,
            }

    return TemplateResponse(request, 'reagent.html', context)

#class SearchReagentView(FormMixin, ListView):
#    model = Reagent
#    form_class = SearchForm
#    template_name = 'reagents_search.html'
#     queryset = Reagent.objects.all()
#     paginate_by = 4
#
#     def get_form_kwargs(self):
#         return {
#           'initial': self.get_initial(),
#           'prefix': self.get_prefix(),
#           'data': self.request.GET or None
#         }
#
#     def get(self, request, *args, **kwargs):
#         GET_params = request.GET.copy()
#         form = self.get_form(self.get_form_class())
#         self.object_list = self.get_queryset()
#
#         if form.is_valid():
#             self.object_list = form.filter_queryset(request, self.object_list)
#         else:
#             self.object_list = []
#
#         context = self.get_context_data(
#             form=form, object_list=self.object_list, active_page='reagent',
#             query=self.request.GET.get('keyword'), GET_params=GET_params)
#
#         return self.render_to_response(context)
#
# search_form_view = login_required(SearchReagentView.as_view())
