import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Services, ServicesForm
from core.security.mixins import GroupPermissionMixin


class ServicesListView(GroupPermissionMixin, TemplateView):
    template_name = 'services/list.html'
    permission_required = 'view_services'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Services.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['create_url'] = reverse_lazy('services_create')
        return context


class ServicesCreateView(GroupPermissionMixin, CreateView):
    model = Services
    template_name = 'services/create.html'
    form_class = ServicesForm
    success_url = reverse_lazy('services_list')
    permission_required = 'add_services'

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
        context['title'] = 'Nuevo registro de un Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ServicesUpdateView(GroupPermissionMixin, UpdateView):
    model = Services
    template_name = 'services/create.html'
    form_class = ServicesForm
    success_url = reverse_lazy('services_list')
    permission_required = 'change_services'

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
        context['title'] = 'Edición de un Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ServicesDeleteView(GroupPermissionMixin, DeleteView):
    model = Services
    template_name = 'delete.html'
    success_url = reverse_lazy('services_list')
    permission_required = 'delete_services'

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
