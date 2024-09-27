import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView

from config import settings
from core.clinic.forms import ClientForm, User, Parish, Client, ClientUserForm, Company
from core.homepage.forms import CommentsForm, Statistics, Services, Departments, Team, Gallery, Qualities, Testimonials, FrequentQuestions


class IndexView(FormView):
    template_name = 'mainpage/index.html'
    form_class = CommentsForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'send_comments':
                form = self.get_form()
                form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f'{Company.objects.first().name} | Control de Veterinaria'
        context['statistics'] = Statistics.objects.filter(state=True).order_by('name')
        context['services'] = Services.objects.filter(state=True).order_by('id').order_by('name')
        context['departments'] = Departments.objects.filter(state=True).order_by('id').order_by('name')
        context['frequent_questions'] = FrequentQuestions.objects.filter(state=True).order_by('id')
        context['testimonials'] = Testimonials.objects.filter(state=True).order_by('id')
        context['gallery'] = Gallery.objects.filter(state=True).order_by('id')
        context['teams'] = Team.objects.filter(state=True).order_by('id')
        context['qualities'] = Qualities.objects.filter(state=True).order_by('id')
        context['initial'] = True
        return context


class SignInView(FormView):
    form_class = ClientForm
    template_name = 'mainpage/sign_in.html'
    success_url = reverse_lazy('index')

    def send_email(self, user):
        ABSOLUTE_ROOT_URL = self.request.build_absolute_uri('/').strip('/')
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Registro de cuenta'
        message['From'] = settings.EMAIL_HOST_USER
        message['To'] = user.email
        parameters = {
            'user': user,
            'company': Company.objects.first(),
            'link_home': ABSOLUTE_ROOT_URL,
            'link_login': f'{ABSOLUTE_ROOT_URL}/login',
        }
        html = render_to_string('mainpage/email_sign_in.html', parameters)
        content = MIMEText(html, 'html')
        message.attach(content)
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, user.email, message.as_string())
        server.quit()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'register':
                with transaction.atomic():
                    dni = request.POST['dni']
                    user = User()
                    user.names = request.POST['names']
                    user.username = dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.username)
                    user.email = request.POST['email']
                    user.save()
                    client = Client()
                    client.user = user
                    client.dni = dni
                    client.parish_id = int(request.POST['parish'])
                    client.gender = request.POST['gender']
                    client.mobile = request.POST['mobile']
                    client.phone = request.POST['phone']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()
                    group = Group.objects.get(pk=settings.GROUPS['client'])
                    user.groups.add(group)
                    self.send_email(user)
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Client.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.get_full_name(), 'data': i.toJSON()}
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de un cliente'
        context['list_url'] = self.success_url
        context['frmUser'] = ClientUserForm()
        return context
