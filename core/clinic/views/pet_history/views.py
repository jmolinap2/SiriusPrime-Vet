import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.forms import Mascot, PetHistoryForm, SaleProduct, HistorialMedical, Sale, MedicalParameter
from core.security.mixins import GroupModuleMixin


class PetHistoryVaccinesListView(GroupModuleMixin, FormView):
    form_class = PetHistoryForm
    template_name = 'pet_history/vaccines.html'

    def get_form(self, form_class=None):
        form = PetHistoryForm()
        if self.request.user.is_client():
            form.fields['mascot'].queryset = Mascot.objects.filter(client__user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                mascot = request.POST['mascot']
                queryset = SaleProduct.objects.filter(medical_control=True)
                if len(mascot):
                    queryset = queryset.filter(sale__mascot_id=mascot)
                for i in queryset:
                    item = i.toJSON()
                    item['sale'] = i.sale.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de Vacunas'
        return context


class PetHistoryMedicalListView(GroupModuleMixin, FormView):
    form_class = PetHistoryForm
    template_name = 'pet_history/medical.html'

    def get_form(self, form_class=None):
        form = PetHistoryForm()
        if self.request.user.is_client():
            form.fields['mascot'].queryset = Mascot.objects.filter(client__user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                mascot = request.POST['mascot']
                if len(mascot):
                    queryset = HistorialMedical.objects.filter(sale__mascot_id=mascot)
                    sale_id = list(queryset.order_by('sale').distinct().values_list('sale_id', flat=True))
                    for i in Sale.objects.filter(id__in=sale_id):
                        item = [i.date_joined_format()]
                        for d in i.historialmedical_set.all():
                            item.append(d.valor)
                        data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial Médico de Mascotas'
        context['medical_parameter'] = MedicalParameter.objects.all()
        return context
