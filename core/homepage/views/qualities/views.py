import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Qualities, QualitiesForm
from core.security.mixins import GroupPermissionMixin


class QualitiesListView(GroupPermissionMixin, TemplateView):
    template_name = 'qualities/list.html'
    permission_required = 'view_qualities'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Qualities.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cualidades'
        context['create_url'] = reverse_lazy('qualities_create')
        return context


class QualitiesCreateView(GroupPermissionMixin, CreateView):
    model = Qualities
    template_name = 'qualities/create.html'
    form_class = QualitiesForm
    success_url = reverse_lazy('qualities_list')
    permission_required = 'add_qualities'

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
        context['title'] = 'Nuevo registro de una Cualidad'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class QualitiesUpdateView(GroupPermissionMixin, UpdateView):
    model = Qualities
    template_name = 'qualities/create.html'
    form_class = QualitiesForm
    success_url = reverse_lazy('qualities_list')
    permission_required = 'change_qualities'

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
        context['title'] = 'Edición de una Cualidad'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class QualitiesDeleteView(GroupPermissionMixin, DeleteView):
    model = Qualities
    template_name = 'delete.html'
    success_url = reverse_lazy('qualities_list')
    permission_required = 'delete_qualities'

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
