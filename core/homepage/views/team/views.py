import json
import os

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Team, TeamForm, TeamSocialNetworks
from core.security.mixins import GroupPermissionMixin


class TeamListView(GroupPermissionMixin, TemplateView):
    template_name = 'team/list.html'
    permission_required = 'view_team'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Team.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Doctores'
        context['create_url'] = reverse_lazy('team_create')
        return context


class TeamCreateView(GroupPermissionMixin, CreateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'add_team'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    team = Team()
                    team.names = request.POST['names']
                    team.job = request.POST['job']
                    team.description = request.POST['description']
                    team.phrase = request.POST['phrase']
                    team.state = 'state' in request.POST
                    if 'image' in request.FILES:
                        team.image = request.FILES['image']
                    team.save()
                    for i in json.loads(request.POST['social_networks']):
                        detail = TeamSocialNetworks()
                        detail.team = team
                        detail.icon = i['icon']
                        detail.name = i['name']
                        detail.url = i['url']
                        detail.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Doctor'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['social_networks'] = []
        return context


class TeamUpdateView(GroupPermissionMixin, UpdateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'change_team'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    team = self.object
                    team.names = request.POST['names']
                    team.job = request.POST['job']
                    team.description = request.POST['description']
                    team.phrase = request.POST['phrase']
                    team.state = 'state' in request.POST
                    if 'image-clear' in request.POST and team.image:
                        os.remove(team.image.path)
                        team.image = None
                    if 'image' in request.FILES:
                        team.image = request.FILES['image']
                    team.save()
                    team.teamsocialnetworks_set.all().delete()
                    for i in json.loads(request.POST['social_networks']):
                        detail = TeamSocialNetworks()
                        detail.team = team
                        detail.icon = i['icon']
                        detail.name = i['name']
                        detail.url = i['url']
                        detail.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Doctor'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['social_networks'] = json.dumps(self.object.get_teamsocialnetworks())
        return context


class TeamDeleteView(GroupPermissionMixin, DeleteView):
    model = Team
    template_name = 'delete.html'
    success_url = reverse_lazy('team_list')
    permission_required = 'delete_team'

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
