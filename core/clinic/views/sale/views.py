import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView
from django.views.generic.base import View

from core.clinic import printer
from core.clinic.forms import SaleForm, Sale, SaleProduct, MedicalParameter, HistorialMedical, Mascot, Product, Company, TYPE_SALE, PRODUCT_TYPE, TYPE_STATUS
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class SaleListView(GroupPermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/admin/list.html'
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Sale.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type_sale = request.POST['type_sale']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                if len(type_sale):
                    queryset = queryset.filter(type=type_sale)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_product':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=False):
                    data.append(i.toJSON())
            elif action == 'search_detail_vaccine':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=True):
                    data.append(i.toJSON())
            elif action == 'search_historial_medical':
                data = []
                for i in HistorialMedical.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        return context


class SaleDeleteView(GroupPermissionMixin, DeleteView):
    model = Sale
    template_name = 'delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            sale = self.get_object()
            sale.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class SalePrintInvoiceView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sale_list')

    def get_success_url(self):
        if self.request.user.is_client():
            return reverse_lazy('sale_client_list')
        return self.success_url

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.filter(id=self.kwargs['pk']).first()
            if sale:
                context = {'sale': sale, 'company': Company.objects.first()}
                pdf_file = printer.create_pdf(context=context, template_name='sale/format/invoice.html')
                return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.get_success_url())


class SaleEmployeeListView(GroupPermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/employee/list.html'
    permission_required = 'view_sale_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Sale.objects.filter(employee__user=request.user)
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type_sale = request.POST['type_sale']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                if len(type_sale):
                    queryset = queryset.filter(type=type_sale)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_product':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=False):
                    data.append(i.toJSON())
            elif action == 'search_detail_vaccine':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=True):
                    data.append(i.toJSON())
            elif action == 'search_historial_medical':
                data = []
                for i in HistorialMedical.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_employee_create')
        return context


class SaleEmployeeCreateView(GroupPermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/employee/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_employee_list')
    permission_required = 'add_sale_employee'

    def get_object(self, queryset=None):
        sale = Sale()
        if 'pk' in self.kwargs:
            sale = Sale.objects.filter(id=self.kwargs['pk']).first()
        return sale

    def get_form(self, form_class=None):
        form = SaleForm()
        instance = self.get_object()
        if instance.pk is None:
            form.fields['mascot'].queryset = Mascot.objects.none()
        else:
            form = SaleForm(instance=instance)
            form.fields['date_joined'].widget.attrs['disabled'] = True
            form.fields['type'].widget.attrs['disabled'] = True
            form.fields['mascot'].widget.attrs['disabled'] = True
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = self.get_object()
                    if sale.pk is None:
                        sale.type = request.POST['type']
                        sale.mascot_id = int(request.POST['mascot'])
                        sale.employee_id = request.user.employee.id
                        sale.date_joined = request.POST['date_joined']
                    if sale.type == TYPE_SALE[2][0]:
                        sale.symptoms = request.POST['symptoms']
                        sale.diagnosis = request.POST['diagnosis']
                        sale.observation = request.POST['observation']
                    sale.iva = float(Company.objects.get().iva) / 100
                    sale.status = TYPE_STATUS[2][0]
                    sale.save()
                    for i in json.loads(request.POST['products']):
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(i['id'])
                        detail.cant = int(i['cant'])
                        detail.price = float(i['pvp'])
                        detail.subtotal = detail.cant * float(detail.price)
                        detail.save()
                        if detail.product.type is not PRODUCT_TYPE[2][0]:
                            detail.product.stock -= detail.cant
                            detail.product.save()
                    if sale.type == TYPE_SALE[2][0]:
                        for i in json.loads(request.POST['vaccines']):
                            detail = SaleProduct()
                            detail.sale_id = sale.id
                            detail.product_id = int(i['id'])
                            detail.date_vaccine = i['date_vaccine']
                            detail.next_date = i['next_date']
                            detail.cant = int(i['cant'])
                            detail.price = float(i['pvp'])
                            detail.subtotal = detail.cant * float(detail.price)
                            detail.medical_control = True
                            if 'image_vaccine' in i:
                                detail.save_image_base64(image_data=i['image_vaccine'])
                            detail.save()
                            if detail.product.type is not PRODUCT_TYPE[2][0]:
                                detail.product.stock -= detail.cant
                                detail.product.save()
                        for i in json.loads(request.POST['medical_parameter']):
                            detail = HistorialMedical()
                            detail.sale_id = sale.id
                            detail.medical_parameter_id = int(i['id'])
                            detail.valor = i['valor']
                            detail.description = i['description']
                            detail.save()
                    sale.calculate_invoice()
                    if sale.get_vaccines().exists():
                        sale.send_reminder_next_vaccine()
                    url_print = reverse_lazy('sale_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(url_print)}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(Q(stock__gt=0) | Q(type=PRODUCT_TYPE[2][0])).exclude(type=PRODUCT_TYPE[1][0]).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_vaccines':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(Q(stock__gt=0), type=PRODUCT_TYPE[1][0]).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))[0:10]
                for i in queryset:
                    item = i.toJSON()
                    current_date = datetime.now().date().strftime('%Y-%m-%d')
                    item['date_vaccine'] = current_date
                    item['next_date'] = current_date
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_mascot':
                data = []
                term = request.POST['term']
                for i in Mascot.objects.filter(Q(client__user__names__icontains=term) | Q(name__icontains=term) | Q(client__dni__icontains=term))[0:10]:
                    item = {'id': i.id, 'text': i.get_full_name()}
                    data.append(item)
            elif action == 'get_medical_history':
                data = []
                mascot_id = request.POST['mascot']
                for i in MedicalParameter.objects.filter():
                    item = i.toJSON()
                    item['last_value'] = i.get_last_value(mascot_id=mascot_id)
                    item['valor'] = '0.00'
                    item['description'] = ''
                    data.append(item)
            elif action == 'search_medical_history':
                data = []
                queryset = HistorialMedical.objects.filter(sale__mascot_id=request.POST['mascot'])
                sale_id = list(queryset.order_by('sale').distinct().values_list('sale_id', flat=True))
                for i in Sale.objects.filter(id__in=sale_id):
                    item = [i.date_joined_format()]
                    for d in i.historialmedical_set.all():
                        item.append(d.valor)
                    data.append(item)
            elif action == 'search_medicines_history':
                data = []
                for i in SaleProduct.objects.filter(medical_control=True, sale__mascot_id=request.POST['mascot']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        context['medical_parameter'] = MedicalParameter.objects.all()
        return context


class SaleEmployeeDeleteView(GroupPermissionMixin, DeleteView):
    model = Sale
    template_name = 'delete.html'
    success_url = reverse_lazy('sale_employee_list')
    permission_required = 'delete_sale_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            sale = self.get_object()
            sale.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class SaleClientListView(GroupPermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/client/list.html'
    permission_required = 'view_sale_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Sale.objects.filter(mascot__client__user=request.user)
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type_sale = request.POST['type_sale']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                if len(type_sale):
                    queryset = queryset.filter(type=type_sale)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'cancel_quote':
                sale = Sale.objects.get(pk=request.POST['id'])
                sale.status = TYPE_STATUS[1][0]
                sale.save()
            elif action == 'search_detail_product':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=False):
                    data.append(i.toJSON())
            elif action == 'search_detail_vaccine':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id'], medical_control=True):
                    data.append(i.toJSON())
            elif action == 'search_historial_medical':
                data = []
                for i in HistorialMedical.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_client_create')
        return context


class SaleClienCreateView(GroupPermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/client/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_client_list')
    permission_required = 'add_sale_client'

    def get_form(self, form_class=None):
        form = SaleForm()
        form.fields['mascot'].queryset = Mascot.objects.filter(client__user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = Sale()
                    sale.type = TYPE_SALE[2][0]
                    sale.mascot_id = int(request.POST['mascot'])
                    sale.employee_id = int(request.POST['employee'])
                    sale.date_joined = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                    sale.hour = datetime.strptime(request.POST['hour'], '%H:%M').time()
                    sale.symptoms = request.POST['symptoms']
                    sale.save()
                    data = {'msg': f"Cita agendada correctamente para el dia {sale.date_joined_format()} a las {sale.hour_format()}"}
            elif action == 'find_scheduling_space':
                data = []
                date_current = datetime.now()
                employee = self.request.POST['employee']
                date_joined = self.request.POST['date_joined']
                if len(employee) and len(date_joined):
                    date_joined = datetime.strptime(date_joined, '%Y-%m-%d')
                    index = 0
                    for i in range(8, 19):
                        hour = i
                        if i < 10:
                            hour = f'0{i}'
                        for minute in ['00', '15', '30', '45']:
                            clock = datetime(year=date_joined.year, month=date_joined.month, day=date_joined.day, hour=int(hour), minute=int(minute))
                            status = 'vacant'
                            if Sale.objects.filter(date_joined=date_joined, employee_id=employee, hour=clock.time(), type=TYPE_STATUS[2][0], status=TYPE_STATUS[0][0]).exists():
                                status = 'reserved'
                            elif date_current > clock:
                                status = 'time_not_available'
                            data.append({'index': index, 'hour': clock.time().strftime('%H:%M'), 'status': status})
                            if i == 18:
                                break
                            index += 1
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Cita Médica'
        context['action'] = 'add'
        return context
