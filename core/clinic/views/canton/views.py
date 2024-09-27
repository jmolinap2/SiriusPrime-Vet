import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Canton, CantonForm
from core.security.mixins import GroupPermissionMixin


class CantonListView(GroupPermissionMixin, TemplateView):
    template_name = 'canton/list.html'
    permission_required = 'view_canton'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Canton.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cantones'
        context['create_url'] = reverse_lazy('canton_create')
        return context


class CantonCreateView(GroupPermissionMixin, CreateView):
    model = Canton
    template_name = 'canton/create.html'
    form_class = CantonForm
    success_url = reverse_lazy('canton_list')
    permission_required = 'add_canton'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Canton.objects.all()
                name = request.POST['name'].strip()
                province = request.POST['province']
                if len(province):
                    data['valid'] = not queryset.filter(name__iexact=name, province_id=province).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Cantón'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CantonUpdateView(GroupPermissionMixin, UpdateView):
    model = Canton
    template_name = 'canton/create.html'
    form_class = CantonForm
    success_url = reverse_lazy('canton_list')
    permission_required = 'change_canton'

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
                queryset = Canton.objects.all().exclude(id=self.get_object().id)
                name = request.POST['name'].strip()
                province = request.POST['province']
                if len(province):
                    data['valid'] = not queryset.filter(name__iexact=name, province_id=province).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Cantón'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CantonDeleteView(GroupPermissionMixin, DeleteView):
    model = Canton
    template_name = 'delete.html'
    success_url = reverse_lazy('canton_list')
    permission_required = 'delete_canton'

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
