from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from qcapp.forms import CellForm
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView
from qcapp.models import Cell, CellPanel
from django.contrib import messages


class CellAllView(ListView):
    model = Cell
    paginate_by = 4
    template_name = 'cell.html'

    def get_context_data(self, **kwargs):
        context = super(CellAllView, self).get_context_data(**kwargs)
        context['active_page'] = 'cellpanel'
        context['cellpanelid'] = self.args[0]
        context['cellpaneltype'] = CellPanel.objects.get(id=self.args[0]).type
        context['keyword'] = self.request.GET.get('keyword')
        GET_params = self.request.GET.copy()
        if 'page' in GET_params:
            del GET_params['page']
        context['GET_params'] = GET_params
        return context

    def get_queryset(self):
        cellpanelid = self.args[0]
        queryset = Cell.objects.filter(cell_panel__id__contains=cellpanelid)

        if 'keyword' in self.request.GET:
            q = self.request.GET['keyword']
            if q:
                queryset = queryset.filter(
                    Q(type__icontains=q) | Q(lot__icontains=q)
                )

        sort_by = self.request.GET.get('sortBy')
        if sort_by == 'expiryDate':
            queryset = queryset.order_by('expiry')
        elif sort_by == 'entryDate':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'lot':
            queryset == queryset.order_by('lot')
        return queryset

cell_view = login_required(CellAllView.as_view())


class CellNewView(FormView):
    template_name = 'cell_new.html'
    form_class = CellForm

    def get_context_data(self, **kwargs):
        context = super(CellNewView, self).get_context_data(**kwargs)
        context['active_page'] = 'cellpanel'
        context['cellpanelid'] = self.args[0]
        context['cellpaneltype'] = CellPanel.objects.get(id=self.args[0]).type
        return context

    def render_to_response(self, context):
        context['active_page'] = 'cellpanel'
        return super().render_to_response(context)

    def form_valid(self, form):
        messages.success(
            self.request, 'You entered a new Cell for' + CellPanel.objects.get(id=self.args[0]).type + 'successfully!')
        new_cell = form.save()
        return HttpResponseRedirect('/cellpanel/%s/cell/%s/' % (self.args[0], new_cell.id))



cell_new_view = login_required(CellNewView.as_view())
#
#
# class IdCardEditView(UpdateView):
#     template_name = 'idcard_edit.html'
#     form_class = IdCardForm
#
#     def get_object(self, queryset=None):
#         obj = IdCard.objects.get(id=self.args[0])
#         return obj
#
#     def get_context_data(self, **kwargs):
#         context = super(IdCardEditView, self).get_context_data(**kwargs)
#         context['active_page'] = 'idcard'
#         return context
#
#     def form_valid(self, form, **kwargs):
#         form.save()
#         messages.success(
#             self.request, 'You changed the IdCard successfully!')
#         return HttpResponseRedirect('/idcard/')
#
# idcard_edit_view = login_required(IdCardEditView.as_view())
#
#
# class IdCardDeleteView(DeleteView):
#     model = IdCard
#     success_url = '/idcard/'
#
#     def get_object(self, queryset=None):
#         obj = IdCard.objects.get(id=self.args[0])
#         messages.success(
#             self.request, 'You deleted the IdCard successfully!')
#         return obj
#
# idcard_delete_record_view = login_required(IdCardDeleteView.as_view())
