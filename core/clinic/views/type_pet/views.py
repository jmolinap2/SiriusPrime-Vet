import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import TypePet, TypePetForm
from core.security.mixins import GroupPermissionMixin


class TypePetListView(GroupPermissionMixin, TemplateView):
    template_name = 'type_pet/list.html'
    permission_required = 'view_type_pet'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in TypePet.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Animales'
        context['create_url'] = reverse_lazy('type_pet_create')
        return context


class TypePetCreateView(GroupPermissionMixin, CreateView):
    model = TypePet
    template_name = 'type_pet/create.html'
    form_class = TypePetForm
    success_url = reverse_lazy('type_pet_list')
    permission_required = 'add_type_pet'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = TypePet.objects.all()
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
        context['title'] = 'Nuevo registro de un Tipo de Animal'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TypePetUpdateView(GroupPermissionMixin, UpdateView):
    model = TypePet
    template_name = 'type_pet/create.html'
    form_class = TypePetForm
    success_url = reverse_lazy('type_pet_list')
    permission_required = 'change_type_pet'

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
                queryset = TypePet.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un Tipo de Animal'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TypePetDeleteView(GroupPermissionMixin, DeleteView):
    model = TypePet
    template_name = 'delete.html'
    success_url = reverse_lazy('type_pet_list')
    permission_required = 'delete_type_pet'

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
