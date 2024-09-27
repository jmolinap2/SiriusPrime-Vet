import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView

from core.homepage.forms import Comments
from core.security.mixins import GroupPermissionMixin


class CommentsListView(GroupPermissionMixin, TemplateView):
    template_name = 'comments/list.html'
    permission_required = 'view_comments'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Comments.objects.all().order_by('-id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Comentarios'
        return context


class CommentsDeleteView(GroupPermissionMixin, DeleteView):
    model = Comments
    template_name = 'delete.html'
    success_url = reverse_lazy('comments_list')
    permission_required = 'delete_comments'

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
