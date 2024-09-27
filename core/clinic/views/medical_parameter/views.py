import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import MedicalParameter, MedicalParameterForm
from core.security.mixins import GroupPermissionMixin


class MedicalParameterListView(GroupPermissionMixin, TemplateView):
    template_name = 'medical_parameter/list.html'
    permission_required = 'view_medical_parameter'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in MedicalParameter.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Parámetros Médicos'
        context['create_url'] = reverse_lazy('medical_parameter_create')
        return context


class MedicalParameterCreateView(GroupPermissionMixin, CreateView):
    model = MedicalParameter
    template_name = 'medical_parameter/create.html'
    form_class = MedicalParameterForm
    success_url = reverse_lazy('medical_parameter_list')
    permission_required = 'add_medical_parameter'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = MedicalParameter.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Parámetro Médico'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class MedicalParameterUpdateView(GroupPermissionMixin, UpdateView):
    model = MedicalParameter
    template_name = 'medical_parameter/create.html'
    form_class = MedicalParameterForm
    success_url = reverse_lazy('medical_parameter_list')
    permission_required = 'change_medical_parameter'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = MedicalParameter.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Parámetro Médico'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class MedicalParameterDeleteView(GroupPermissionMixin, DeleteView):
    model = MedicalParameter
    template_name = 'delete.html'
    success_url = reverse_lazy('medical_parameter_list')
    permission_required = 'delete_medical_parameter'

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
