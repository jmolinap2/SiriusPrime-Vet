import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import Profession, ProfessionForm
from core.security.mixins import GroupPermissionMixin


class ProfessionListView(GroupPermissionMixin, TemplateView):
    template_name = 'profession/list.html'
    permission_required = 'view_profession'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Profession.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Profesiones'
        context['create_url'] = reverse_lazy('profession_create')
        return context


class ProfessionCreateView(GroupPermissionMixin, CreateView):
    model = Profession
    template_name = 'profession/create.html'
    form_class = ProfessionForm
    success_url = reverse_lazy('profession_list')
    permission_required = 'add_profession'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Profession.objects.all()
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
        context['title'] = 'Nuevo registro de una Profesión'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProfessionUpdateView(GroupPermissionMixin, UpdateView):
    model = Profession
    template_name = 'profession/create.html'
    form_class = ProfessionForm
    success_url = reverse_lazy('profession_list')
    permission_required = 'change_profession'

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
                queryset = Profession.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una Profesión'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProfessionDeleteView(GroupPermissionMixin, DeleteView):
    model = Profession
    template_name = 'delete.html'
    success_url = reverse_lazy('profession_list')
    permission_required = 'delete_profession'

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
