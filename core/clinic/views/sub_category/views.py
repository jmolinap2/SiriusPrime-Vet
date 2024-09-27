import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.clinic.forms import SubCategory, SubCategoryForm
from core.security.mixins import GroupPermissionMixin


class SubCategoryListView(GroupPermissionMixin, TemplateView):
    template_name = 'sub_category/list.html'
    permission_required = 'view_sub_category'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in SubCategory.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de SubCategorías'
        context['create_url'] = reverse_lazy('sub_category_create')
        return context


class SubCategoryCreateView(GroupPermissionMixin, CreateView):
    model = SubCategory
    template_name = 'sub_category/create.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('sub_category_list')
    permission_required = 'add_sub_category'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = SubCategory.objects.all()
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
        context['title'] = 'Nuevo registro de una SubCategoría'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SubCategoryUpdateView(GroupPermissionMixin, UpdateView):
    model = SubCategory
    template_name = 'sub_category/create.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('sub_category_list')
    permission_required = 'change_sub_category'

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
                queryset = SubCategory.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una SubCategoría'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class SubCategoryDeleteView(GroupPermissionMixin, DeleteView):
    model = SubCategory
    template_name = 'delete.html'
    success_url = reverse_lazy('sub_category_list')
    permission_required = 'delete_sub_category'

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
