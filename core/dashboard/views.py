import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.clinic.choices import PRODUCT_TYPE
from core.clinic.models import Provider, Mascot, Product, SaleProduct, Sale, Category, Client
from core.homepage.models import Videos, News
from core.reports.choices import MONTHS
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        dashboard = Dashboard.objects.first()
        if dashboard and dashboard.layout == 1:
            return 'vtc_dashboard.html'
        return 'hzt_dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_sales_products_year_month':
                data = []
                year = datetime.now().year
                month = datetime.now().month
                for i in Product.objects.all():
                    total = SaleProduct.objects.exclude(product__type=PRODUCT_TYPE[2][0]).filter(sale__date_joined__year=year, sale__date_joined__month=month, product_id=i.id).aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result']
                    if total > 0:
                        data.append({'name': i.name, 'y': float(total)})
            elif action == 'get_graph_sales_year_month':
                data = []
                year = datetime.now().year
                for i in range(1, 13):
                    total = Sale.objects.filter(date_joined__year=year, date_joined__month=i).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField()))['result']
                    data.append(float(total))
            elif action == 'get_graph_sales_category':
                data = []
                year = datetime.now().year
                month = datetime.now().month
                for i in Category.objects.all():
                    total = SaleProduct.objects.exclude(product__type=PRODUCT_TYPE[2][0]).filter(sale__date_joined__year=year, sale__date_joined__month=month, product__category_id=i.id).aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result']
                    data.append({'name': i.name, 'y': float(total)})
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        if self.request.user.is_client():
            context['clients'] = Client.objects.all().count()
            context['providerS'] = Provider.objects.all().count()
            context['mascotS'] = Mascot.objects.all().count()
            context['products'] = Product.objects.all().count()
            context['month'] = MONTHS[datetime.now().date().month][1]
        else:
            context['videos'] = Videos.objects.filter(state=True)
            context['news'] = News.objects.filter(state=True)
        return context
