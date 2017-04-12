from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from qcapp.forms import IdCardForm
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView
from qcapp.models import CellPanel
from django.contrib import messages


class CellPanelAllView(ListView):
    model = CellPanel
    paginate_by = 4
    template_name = 'cellpanel.html'

    def get_context_data(self, **kwargs):
        context = super(CellPanelAllView, self).get_context_data(**kwargs)
        context['active_page'] = 'cellpanel'
        context['keyword'] = self.request.GET.get('keyword')
        GET_params = self.request.GET.copy()
        if 'page' in GET_params:
            del GET_params['page']
        context['GET_params'] = GET_params
        return context

    def get_queryset(self):
        queryset = CellPanel.objects.all()

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

cellpanel_view = login_required(CellPanelAllView.as_view())


# class IdCardNewView(FormView):
#     template_name = 'idcard_new.html'
#     form_class = IdCardForm
#
#     def render_to_response(self, context):
#         context['active_page'] = 'idcard'
#         return super().render_to_response(context)
#
#     def form_valid(self, form):
#         form.save()
#         messages.success(
#             self.request, 'You entered a new IdCard successfully!')
#         return HttpResponseRedirect('/idcard/')
#
# idcard_new_view = login_required(IdCardNewView.as_view())
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
