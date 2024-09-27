import base64
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.clinic.choices import *
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    proprietor = models.CharField(max_length=100, verbose_name='Propietario')
    description = models.CharField(max_length=2000, blank=True, null=True, verbose_name='Descripción')
    with_us = models.CharField(max_length=2000, blank=True, null=True, verbose_name='¿Porque estar con nosotros?')
    mission = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Misión')
    vision = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Visión')
    about_us = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Quienes Somos')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Logo')
    phone = models.CharField(max_length=9, unique=True, blank=True, null=True, verbose_name='Teléfono Convencional')
    mobile = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='Teléfono Celular')
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True, verbose_name='Correo Electrónico')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    horary = models.CharField(max_length=50, blank=True, null=True, verbose_name='Horario')
    latitude = models.CharField(max_length=100, verbose_name='Latitud')
    longitude = models.CharField(max_length=100, verbose_name='Longitud')
    about_youtube = models.CharField(max_length=250, blank=True, null=True, verbose_name='Video de Youtube')
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='IVA')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_full_path_image(self):
        if self.image:
            return self.image.path
        return f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/empty.png'

    def get_iva(self):
        return float(self.iva)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can view Empresa'),
        )


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='País')
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'País: {self.country.name} / Provincia: {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        item['country'] = self.country.toJSON()
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'


class Canton(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='Provincia')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.province.get_full_name()} / Cantón: {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        item['province'] = self.province.toJSON()
        return item

    class Meta:
        verbose_name = 'Cantón'
        verbose_name_plural = 'Cantones'


class Parish(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.PROTECT, verbose_name='Cantón')
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.canton.get_full_name()} / Parroquia: {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        item['canton'] = self.canton.toJSON()
        return item

    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'


class Profession(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Profesión'
        verbose_name_plural = 'Profesiones'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    dni = models.CharField(max_length=13, unique=True, verbose_name='Número de documento')
    gender = models.CharField(max_length=10, choices=GENDER_PERSON, default=GENDER_PERSON[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=7, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parroquia')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.names} / {self.dni}'

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['parish'] = {} if self.parish is None else self.parish.toJSON()
        return item

    def delete(self, using=None, keep_parents=False):
        super(Client, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    dni = models.CharField(max_length=13, unique=True, verbose_name='Número de documento')
    gender = models.CharField(max_length=10, choices=GENDER_PERSON, default=GENDER_PERSON[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=7, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, verbose_name='Parroquia')
    profession = models.ForeignKey(Profession, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Profesión')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.names} / {self.dni} / {self.profession.name}'

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        item['user'] = self.user.toJSON()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['parish'] = {} if self.parish is None else self.parish.toJSON()
        item['profession'] = {} if self.profession is None else self.profession.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.ruc})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'SubCategoría'
        verbose_name_plural = 'SubCategorias'
        default_permissions = ()
        permissions = (
            ('view_sub_category', 'Can view SubCategoría'),
            ('add_sub_category', 'Can add SubCategoría'),
            ('change_sub_category', 'Can add SubCategoría'),
            ('delete_sub_category', 'Can delete SubCategoría'),
        )


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    sub_category = models.ManyToManyField(SubCategory, verbose_name='Subcategoría')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} {self.get_subcategories()}'

    def get_subcategories(self):
        text = ''
        for i in self.sub_category.all():
            text += i.name + ','
        if len(text):
            text = '(' + text[0:-1] + ')'
        return text

    def toJSON(self):
        item = model_to_dict(self)
        item['sub_category'] = [i.toJSON() for i in self.sub_category.all()]
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    type = models.CharField(max_length=25, choices=PRODUCT_TYPE, default=PRODUCT_TYPE[0][0], verbose_name='Tipo de Producto')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Compra')
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    def get_benefit(self):
        benefit = float(self.pvp) - float(self.price)
        return round(benefit, 2)

    def get_full_name(self):
        return f'{self.name} ({self.code}) ({self.category.name})'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['price'] = float(self.price)
        item['pvp'] = float(self.pvp)
        item['category'] = self.category.toJSON()
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['image'] = self.get_image()
        item['benefit'] = float(self.get_benefit())
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(Product, self).save()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Purchase(models.Model):
    number = models.CharField(max_length=8, unique=True, verbose_name='Número de factura')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name='Proveedor')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Subtotal')

    def __str__(self):
        return self.provider.name

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.purchasedetail_set.all():
            subtotal += float(i.price) * int(i.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchasedetail_set.filter(product__inventoried=True):
                i.product.stock -= i.cant
                i.product.save()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro'] = f'{self.id:06d}'
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compras'),
            ('add_purchase', 'Can add Compras'),
            ('delete_purchase', 'Can delete Compras'),
        )


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['product'] = self.product.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Det.Compra'
        verbose_name_plural = 'Det.Compras'
        default_permissions = ()


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    hex = models.CharField(max_length=50, verbose_name='Código')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'


class TypePet(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Mascota'
        verbose_name_plural = 'Tipo de Mascotas'
        default_permissions = ()
        permissions = (
            ('view_type_pet', 'Can view Tipo de Mascota'),
            ('add_type_pet', 'Can add Tipo de Mascota'),
            ('change_type_pet', 'Can change Tipo de Mascota'),
            ('delete_type_pet', 'Can delete Tipo de Mascota'),
        )


class BreedPet(models.Model):
    type_pet = models.ForeignKey(TypePet, on_delete=models.PROTECT, verbose_name='Tipo de Mascota')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.type_pet.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['type_pet'] = self.type_pet.toJSON()
        return item

    class Meta:
        verbose_name = 'Raza de Mascota'
        verbose_name_plural = 'Razas de Mascotas'
        default_permissions = ()
        permissions = (
            ('view_breed_pet', 'Can view Raza de Mascota'),
            ('add_breed_pet', 'Can add Raza de Mascota'),
            ('change_breed_pet', 'Can change Raza de Mascota'),
            ('delete_breed_pet', 'Can delete Raza de Mascota'),
        )


class Mascot(models.Model):
    date_joined = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Cliente')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, verbose_name='Color')
    image = models.ImageField(upload_to='mascot/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    breed_pet = models.ForeignKey(BreedPet, on_delete=models.PROTECT, verbose_name='Tipo de Raza')
    gender = models.CharField(max_length=10, choices=GENDER_PET, default=GENDER_PET[0][0], verbose_name='Sexo')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de cumpleaños')
    observation = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Observación')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'Nombre: {self.name} / Dueño: {self.client.get_full_name()} / Raza: {self.breed_pet.name} / Tipo: {self.breed_pet.type_pet.name} / Color: {self.color.name}'

    def short_name(self):
        return f'Nombre: {self.name} / Raza: {self.breed_pet.name} / Tipo: {self.breed_pet.type_pet.name} / Color: {self.color.name}'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_age(self):
        age = datetime.now().year - self.birthdate.year
        return age

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['breed_pet'] = self.breed_pet.toJSON()
        item['color'] = self.color.toJSON()
        item['client'] = self.client.toJSON()
        item['image'] = self.get_image()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['age'] = self.get_age()
        return item

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        default_permissions = ()
        permissions = (
            ('view_mascot', 'Can view Mascota | Admin'),
            ('add_mascot', 'Can add Mascota | Admin'),
            ('change_mascot', 'Can change Mascota | Admin'),
            ('delete_mascot', 'Can delete Mascota | Admin'),
            ('view_mascot_client', 'Can view Mascota | Cliente'),
            ('add_mascot_client', 'Can add Mascota | Cliente'),
            ('change_mascot_client', 'Can change Mascota | Cliente'),
            ('delete_mascot_client', 'Can delete Mascota | Cliente'),
        )


class MedicalParameter(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def get_last_value(self, mascot_id):
        if len(mascot_id):
            historial_medical = HistorialMedical.objects.filter(sale__mascot_id=mascot_id, medical_parameter_id=self.id).order_by('-id').first()
            if historial_medical:
                return historial_medical.valor
        return '---'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Parámetro Médico'
        verbose_name_plural = 'Parámetros Médicos'
        default_permissions = ()
        permissions = (
            ('view_medical_parameter', 'Can view Parámetro Médico'),
            ('add_medical_parameter', 'Can add Parámetro Médico'),
            ('change_medical_parameter', 'Can change Parámetro Médico'),
            ('delete_medical_parameter', 'Can delete Parámetro Médico'),
        )


class Sale(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    mascot = models.ForeignKey(Mascot, on_delete=models.PROTECT, verbose_name='Mascota')
    type = models.CharField(max_length=50, choices=TYPE_SALE, default='venta', verbose_name='Tipo')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de registro')
    observation = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Observación')
    symptoms = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Síntomas')
    diagnosis = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Diagnóstico')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Iva')
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total iva')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total a pagar')
    status = models.CharField(max_length=30, choices=TYPE_STATUS, default=TYPE_STATUS[0][0], verbose_name='Estado')

    def __str__(self):
        return self.mascot.name

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.saleproduct_set.filter().exclude(product__type=PRODUCT_TYPE[2][0]):
            subtotal += float(i.price) * int(i.cant)
        self.subtotal = subtotal
        self.total_iva = float(self.iva) * float(self.subtotal)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def get_number(self):
        return f'{self.id:06d}'

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def hour_format(self):
        return self.hour.strftime('%H:%M %p')

    def get_products(self):
        return self.saleproduct_set.all().filter(medical_control=False)

    def get_vaccines(self):
        return self.saleproduct_set.all().filter(medical_control=True)

    def get_subtotal_products(self):
        return float(self.get_products().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result'])

    def get_vaccines_products(self):
        return float(self.get_vaccines().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result'])

    def send_reminder_next_vaccine(self):
        try:
            message = MIMEMultipart()
            message['Subject'] = f'Recordatorio de próxima vacuna de tu mascota {self.mascot.name}'
            message['From'] = settings.EMAIL_HOST_USER
            user = self.mascot.client.user
            message['To'] = user.email
            html = f'Sr. {user.names}<br><br>Le notificamos que el día de hoy {self.date_joined_format()} se le puso a su mascota {self.mascot.name} las siguientes vacunas:<br>'
            for index, i in enumerate(self.get_vaccines()):
                html += f'{index + 1}).- Se aplico el {i.product.get_type_display().lower()} {i.product.name} el día {i.date_vaccine_format()}, su próxima vacuna sera el día {i.next_date_format()}.<br>'
            html += f'<br><br>Muchas gracias por su atención<br><br>Que tenga un excelente día Sr. {user.names}'
            content = MIMEText(html, 'html')
            message.attach(content)
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, user.email, message.as_string())
            server.quit()
        except:
            pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.symptoms is None:
            self.symptoms = 's/n'
        elif len(self.symptoms) == 0:
            self.symptoms = 's/n'
        if self.diagnosis is None:
            self.diagnosis = 's/n'
        elif len(self.diagnosis) == 0:
            self.diagnosis = 's/n'
        if self.observation is None:
            self.observation = 's/n'
        elif len(self.observation) == 0:
            self.observation = 's/n'
        super(Sale, self).save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.saleproduct_set.filter().exclude(product_type=PRODUCT_TYPE[2][0]):
                i.product.stock += i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        item['employee'] = self.employee.toJSON()
        item['hour'] = self.hour_format()
        item['mascot'] = self.mascot.toJSON()
        item['date_joined'] = self.date_joined_format()
        item['subtotal'] = float(self.subtotal)
        item['iva'] = float(self.iva)
        item['total'] = float(self.total)
        item['total_iva'] = float(self.total_iva)
        item['historial_medical'] = [i.toJSON() for i in self.historialmedical_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Venta | Admin'),
            ('delete_sale', 'Can delete Venta | Admin'),
            ('view_sale_client', 'Can view Venta | Client'),
            ('add_sale_client', 'Can add Venta | Client'),
            ('view_sale_employee', 'Can view Venta | Employee'),
            ('add_sale_employee', 'Can add Venta | Employee'),
            ('delete_sale_employee', 'Can delete Venta | Employee'),
            ('attend_sale_employee', 'Can attend Venta | Employee'),
        )


class HistorialMedical(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    medical_parameter = models.ForeignKey(MedicalParameter, on_delete=models.PROTECT)
    valor = models.CharField(max_length=100)
    description = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.sale.mascot.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['medical_parameter'] = self.medical_parameter.toJSON()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(HistorialMedical, self).save()

    class Meta:
        verbose_name = 'Historial Médico'
        verbose_name_plural = 'Historiales Médicos'
        default_permissions = ()


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date_vaccine = models.DateField(default=datetime.now)
    next_date = models.DateField(default=datetime.now)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    vaccine_image = models.ImageField(upload_to='sale_product/%Y/%m/%d', null=True, blank=True)
    medical_control = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    def save_image_base64(self, image_data):
        format, image_base_64 = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(image_base_64))
        file_name = f"'vaccine_{datetime.now().date().strftime('%d_%m_%Y_%H_%M')}.{ext}"
        self.vaccine_image.save(file_name, data, save=True)

    def date_vaccine_format(self):
        return self.date_vaccine.strftime('%Y-%m-%d')

    def next_date_format(self):
        return self.next_date.strftime('%Y-%m-%d')

    def get_vaccine_image(self):
        if self.vaccine_image:
            return f'{settings.MEDIA_URL}{self.vaccine_image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        item['date_vaccine'] = self.date_vaccine_format()
        item['next_date'] = self.next_date_format()
        item['vaccine_image'] = self.get_vaccine_image()
        return item

    class Meta:
        verbose_name = 'Venta de Producto'
        verbose_name_plural = 'Venta de Productos'
        default_permissions = ()
