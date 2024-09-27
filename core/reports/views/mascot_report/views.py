import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.reports.forms import ReportForm, Mascot
from core.security.mixins import GroupModuleMixin


class MascotReportView(GroupModuleMixin, FormView):
    template_name = 'mascot_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = request.POST['term']
                breed_pet = request.POST['breed_pet']
                queryset = Mascot.objects.filter()
                if len(term):
                    queryset = queryset.filter(name__icontains=term)
                if len(breed_pet):
                    queryset = queryset.filter(breed_pet_id=breed_pet)
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Mascotas'
        return context
