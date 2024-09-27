import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Parish, ParishForm
from core.security.mixins import GroupPermissionMixin


class ParishListView(GroupPermissionMixin, TemplateView):
    template_name = 'parish/list.html'
    permission_required = 'view_parish'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Parish.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Parroquias'
        context['create_url'] = reverse_lazy('parish_create')
        return context


class ParishCreateView(GroupPermissionMixin, CreateView):
    model = Parish
    template_name = 'parish/create.html'
    form_class = ParishForm
    success_url = reverse_lazy('parish_list')
    permission_required = 'add_parish'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Parish.objects.all()
                name = request.POST['name'].strip()
                canton = request.POST['canton']
                if len(canton):
                    data['valid'] = not queryset.filter(name__iexact=name, canton_id=canton).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Parroquia'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ParishUpdateView(GroupPermissionMixin, UpdateView):
    model = Parish
    template_name = 'parish/create.html'
    form_class = ParishForm
    success_url = reverse_lazy('parish_list')
    permission_required = 'change_parish'

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
                queryset = Parish.objects.all().exclude(id=self.get_object().id)
                name = request.POST['name'].strip()
                canton = request.POST['canton']
                if len(canton):
                    data['valid'] = not queryset.filter(name__iexact=name, canton_id=canton).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Parroquia'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ParishDeleteView(GroupPermissionMixin, DeleteView):
    model = Parish
    template_name = 'delete.html'
    success_url = reverse_lazy('parish_list')
    permission_required = 'delete_parish'

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
