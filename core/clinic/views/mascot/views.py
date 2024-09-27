import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, TemplateView

from core.clinic.forms import Mascot, MascotForm
from core.security.mixins import GroupPermissionMixin


class MascotListView(GroupPermissionMixin, FormView):
    form_class = MascotForm
    template_name = 'mascot/admin/list.html'
    permission_required = 'view_mascot'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                client = request.POST['client']
                queryset = Mascot.objects.filter()
                if len(client):
                    queryset = queryset.filter(client_id=client)
                for i in queryset.order_by('id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Mascotas'
        context['create_url'] = reverse_lazy('mascot_create')
        return context


class MascotCreateView(GroupPermissionMixin, CreateView):
    model = Mascot
    template_name = 'mascot/admin/create.html'
    form_class = MascotForm
    success_url = reverse_lazy('mascot_list')
    permission_required = 'add_mascot'

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
        context['title'] = 'Nuevo registro de una Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class MascotUpdateView(GroupPermissionMixin, UpdateView):
    model = Mascot
    template_name = 'mascot/admin/create.html'
    form_class = MascotForm
    success_url = reverse_lazy('mascot_list')
    permission_required = 'change_mascot'

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
        context['title'] = 'Nuevo registro de una Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class MascotDeleteView(GroupPermissionMixin, DeleteView):
    model = Mascot
    template_name = 'delete.html'
    success_url = reverse_lazy('mascot_list')
    permission_required = 'delete_mascot'

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


class MascotClientListView(GroupPermissionMixin, TemplateView):
    template_name = 'mascot/client/list.html'
    permission_required = 'view_mascot_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Mascot.objects.filter(client__user=request.user)
                for i in queryset.order_by('id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Mascotas'
        context['create_url'] = reverse_lazy('mascot_client_create')
        return context


class MascotClientCreateView(GroupPermissionMixin, CreateView):
    model = Mascot
    template_name = 'mascot/client/create.html'
    form_class = MascotForm
    success_url = reverse_lazy('mascot_client_list')
    permission_required = 'add_mascot_client'

    def get_form(self, form_class=None):
        form = super(MascotClientCreateView, self).get_form(form_class)
        del form.fields['client']
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                form = self.get_form()
                form.instance.client_id = request.user.client.id
                data = form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class MascotClientUpdateView(GroupPermissionMixin, UpdateView):
    model = Mascot
    template_name = 'mascot/client/create.html'
    form_class = MascotForm
    success_url = reverse_lazy('mascot_client_list')
    permission_required = 'change_mascot_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(MascotClientUpdateView, self).get_form(form_class)
        del form.fields['client']
        return form

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
        context['title'] = 'Nuevo registro de una Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class MascotClientDeleteView(GroupPermissionMixin, DeleteView):
    model = Mascot
    template_name = 'delete.html'
    success_url = reverse_lazy('mascot_client_list')
    permission_required = 'delete_mascot_client'

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
