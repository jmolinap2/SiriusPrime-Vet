import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.reports.forms import ReportForm, Product, PRODUCT_TYPE
from core.security.mixins import GroupModuleMixin


class EarningsReportView(GroupModuleMixin, FormView):
    template_name = 'earnings_report/report.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = ReportForm()
        form.fields['product'].queryset = Product.objects.filter().exclude(type=PRODUCT_TYPE[2][0])
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                product_id = json.loads(request.POST['product_id'])
                queryset = Product.objects.all()
                if len(product_id):
                    queryset = queryset.filter(id__in=product_id)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_graph':
                product_id = json.loads(request.POST['product_id'])
                queryset = Product.objects.all().order_by('name')
                if len(product_id):
                    queryset = queryset.filter(id__in=product_id)
                categories = [i.name for i in queryset]
                series = []
                series.append({'name': 'P./Compra', 'data': [float(i.price) for i in queryset]})
                series.append({'name': 'P./Venta', 'data': [float(i.pvp) for i in queryset]})
                series.append({'name': 'Ganancia', 'data': [float(i.get_benefit()) for i in queryset]})
                data = {'categories': categories, 'series': series}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ganancias'
        return context
