import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import BreedPet, BreedPetForm
from core.security.mixins import GroupPermissionMixin


class BreedPetListView(GroupPermissionMixin, TemplateView):
    template_name = 'breed_pet/list.html'
    permission_required = 'view_breed_pet'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in BreedPet.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Razas de Animales'
        context['create_url'] = reverse_lazy('breed_pet_create')
        return context


class BreedPetCreateView(GroupPermissionMixin, CreateView):
    model = BreedPet
    template_name = 'breed_pet/create.html'
    form_class = BreedPetForm
    success_url = reverse_lazy('breed_pet_list')
    permission_required = 'add_breed_pet'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                type_pet = request.POST['type_pet']
                name = request.POST['name'].strip()
                queryset = BreedPet.objects.all()
                data['valid'] = not queryset.filter(name__iexact=name, type_pet_id=type_pet).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Tipo de Raza de Animal'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BreedPetUpdateView(GroupPermissionMixin, UpdateView):
    model = BreedPet
    template_name = 'breed_pet/create.html'
    form_class = BreedPetForm
    success_url = reverse_lazy('breed_pet_list')
    permission_required = 'change_breed_pet'

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
                type_pet = request.POST['type_pet']
                name = request.POST['name'].strip()
                queryset = BreedPet.objects.all().exclude(id=self.get_object().id)
                data['valid'] = not queryset.filter(name__iexact=name, type_pet_id=type_pet).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Tipo de Raza de Animal'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class BreedPetDeleteView(GroupPermissionMixin, DeleteView):
    model = BreedPet
    template_name = 'delete.html'
    success_url = reverse_lazy('breed_pet_list')
    permission_required = 'delete_breed_pet'

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
