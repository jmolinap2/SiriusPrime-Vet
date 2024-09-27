import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Color, ColorForm
from core.security.mixins import GroupPermissionMixin


class ColorListView(GroupPermissionMixin, TemplateView):
    template_name = 'color/list.html'
    permission_required = 'view_color'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Color.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Colores'
        context['create_url'] = reverse_lazy('color_create')
        return context


class ColorCreateView(GroupPermissionMixin, CreateView):
    model = Color
    template_name = 'color/create.html'
    form_class = ColorForm
    success_url = reverse_lazy('color_list')
    permission_required = 'add_color'

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
        context['title'] = 'Nuevo registro de un Color'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ColorUpdateView(GroupPermissionMixin, UpdateView):
    model = Color
    template_name = 'color/create.html'
    form_class = ColorForm
    success_url = reverse_lazy('color_list')
    permission_required = 'change_color'

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
        context['title'] = 'Edición de un Color'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ColorDeleteView(GroupPermissionMixin, DeleteView):
    model = Color
    template_name = 'delete.html'
    success_url = reverse_lazy('color_list')
    permission_required = 'delete_color'

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
