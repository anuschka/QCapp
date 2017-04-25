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
        new_cell = form.save(commit=False)
        new_cell.cell_panel = CellPanel.objects.get(id=self.args[0])
        try:
            new_cell.save()
            messages.success(
                self.request, 'You entered a new Cell for Cell Panel "' +
                CellPanel.objects.get(id=self.args[0]).type +
                '" successfully!')
            return HttpResponseRedirect('/cellpanel/%s/' % self.args[0])
            #return HttpResponseRedirect('/cellpanel/%s/cell/%s/' % (self.args[0], new_cell.id))
        except:
            form.add_error('number', 'You entered an existing Cell')
            return self.form_invalid(form)


cell_new_view = login_required(CellNewView.as_view())


class CellPanelCellEditView(UpdateView):
    template_name = 'cell_edit.html'
    form_class = CellForm

    def get_object(self, queryset=None):
        cell_panel = CellPanel.objects.get(id=self.args[0])
        cell = Cell.objects.get(id=self.args[1], cell_panel=cell_panel)
        return cell

    def get_context_data(self, **kwargs):
        context = super(CellPanelCellEditView, self).get_context_data(**kwargs)
        context['active_page'] = 'cellpanel'
        context['cellpanelid'] = self.args[0]
        context['cellpaneltype'] = CellPanel.objects.get(id=self.args[0]).type
        return context

    def form_valid(self, form):
        new_cell = form.save(commit=False)
        new_cell.cell_panel = CellPanel.objects.get(id=self.args[0])
        try:
            new_cell.save()
            messages.success(
                self.request, 'You changed Cell no: ' + self.args[1] +
                ' in Cell Panel: ' +
                CellPanel.objects.get(id=self.args[0]).type +
                ' successfully!')
            return HttpResponseRedirect('/cellpanel/%s/' % self.args[0])
            #return HttpResponseRedirect('/cellpanel/%s/cell/%s/' % (self.args[0], new_cell.id))
        except:
            form.add_error('number', 'You entered an existing Cell')
            return self.form_invalid(form)

cellpanel_cell_edit_view = login_required(CellPanelCellEditView.as_view())


class CellDeleteView(DeleteView):
    model = Cell
    success_url = '/cellpanel/%s/' % self.args[0]

    def get_object(self, queryset=None):
        cell_panel = CellPanel.objects.get(id=self.args[0])
        cell = Cell.objects.get(id=self.args[1], cell_panel=cell_panel)
        messages.success(
            self.request, 'You deleted the Cell successfully!')
        return cell

cellpanel_cell_delete_view = login_required(CellDeleteView.as_view())
