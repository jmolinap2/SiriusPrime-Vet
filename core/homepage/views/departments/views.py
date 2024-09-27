import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Departments, DepartmentsForm
from core.security.mixins import GroupPermissionMixin


class DepartmentsListView(GroupPermissionMixin, TemplateView):
    template_name = 'departments/list.html'
    permission_required = 'view_departments'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Departments.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Departamentos'
        context['create_url'] = reverse_lazy('departments_create')
        return context


class DepartmentsCreateView(GroupPermissionMixin, CreateView):
    model = Departments
    template_name = 'departments/create.html'
    form_class = DepartmentsForm
    success_url = reverse_lazy('departments_list')
    permission_required = 'add_departments'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Departamento'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class DepartmentsUpdateView(GroupPermissionMixin, UpdateView):
    model = Departments
    template_name = 'departments/create.html'
    form_class = DepartmentsForm
    success_url = reverse_lazy('departments_list')
    permission_required = 'change_departments'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Departamento'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class DepartmentsDeleteView(GroupPermissionMixin, DeleteView):
    model = Departments
    template_name = 'delete.html'
    success_url = reverse_lazy('departments_list')
    permission_required = 'delete_departments'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
