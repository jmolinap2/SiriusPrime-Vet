from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config import settings


class Services(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='services/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'


class Departments(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    title = models.CharField(max_length=150, verbose_name='Subtítulo')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='departments/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Departmento'
        verbose_name_plural = 'Departmentos'


class FrequentQuestions(models.Model):
    question = models.CharField(max_length=500, verbose_name='Pregunta')
    answer = models.TextField(verbose_name='Respuesta')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.question

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'
        default_permissions = ()
        permissions = (
            ('view_frequent_questions', 'Can view Pregunta Frecuente'),
            ('add_frequent_questions', 'Can add Pregunta Frecuente'),
            ('change_frequent_questions', 'Can change Pregunta Frecuente'),
            ('delete_frequent_questions', 'Can delete Pregunta Frecuente'),
        )


class Testimonials(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    job = models.CharField(max_length=150, verbose_name='Profesión')
    description = models.CharField(max_length=5000, verbose_name='Descripción')
    image = models.ImageField(upload_to='testimonials/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.names

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Testimonios'
        verbose_name_plural = 'Testimonio'


class Gallery(models.Model):
    date_joined = models.DateField(default=datetime.now)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.image.url

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Galería'
        verbose_name_plural = 'Galerias'


class Comments(models.Model):
    names = models.CharField(max_length=100, verbose_name='Nombres')
    email = models.CharField(max_length=150, verbose_name='Email')
    mobile = models.CharField(max_length=15, verbose_name='Teléfono')
    message = models.CharField(max_length=2000, verbose_name='Mensaje')

    def __str__(self):
        return self.message

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        default_permissions = ()
        permissions = (
            ('view_comments', 'Can view Comentario'),
            ('delete_comments', 'Can delete Comentario'),
        )


class SocialNetworks(models.Model):
    css = models.CharField(max_length=50, verbose_name='Nombre de la clase css')
    icon = models.CharField(max_length=100, verbose_name='Icono font-awesome')
    url = models.CharField(max_length=150, verbose_name='Enlace')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.css

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    def toJSON(self):
        item = model_to_dict(self)
        item['icon'] = self.get_icon()
        return item

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'
        default_permissions = ()
        permissions = (
            ('view_social_networks', 'Can view Red Social'),
            ('add_social_networks', 'Can add Red Social'),
            ('change_social_networks', 'Can change Red Social'),
            ('delete_social_networks', 'Can delete Red Social'),
        )


class Statistics(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='statistics/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Estadística'
        verbose_name_plural = 'Estadísticas'


class Team(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    phrase = models.CharField(max_length=5000, verbose_name='Frase')
    job = models.CharField(max_length=150, verbose_name='Profesión')
    image = models.ImageField(upload_to='team/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    description = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Descripción')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.names

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def short_name(self):
        names = self.names.split(' ')
        if len(names) == 4:
            return f'{names[0]} {names[3]}'
        return self.names

    def get_teamsocialnetworks(self):
        data = []
        for i in self.teamsocialnetworks_set.all():
            data.append(i.toJSON())
        return data

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['teamsocialnetworks'] = self.get_teamsocialnetworks()
        return item

    class Meta:
        verbose_name = 'Equipo de Trabajo'
        verbose_name_plural = 'Equipos de Trabajo'


class TeamSocialNetworks(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=50)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['team'])
        return item

    class Meta:
        verbose_name = 'Equipo de Trabajo / Red Social'
        verbose_name_plural = 'Equipos de Trabajo / Redes Sociales'
        default_permissions = ()


class Qualities(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='qualities/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Cualidad'
        verbose_name_plural = 'Cualidades'


class News(models.Model):
    date_joined = models.DateField(default=datetime.now)
    title = models.CharField(max_length=250, verbose_name='Título')
    description = models.CharField(max_length=5000, verbose_name='Descripción')
    image = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='Imagen')
    url = models.TextField(verbose_name='Enlace web')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return str(self.title)

    def trim_desc(self):
        return self.description[0:150]

    def url_short(self):
        return self.url[0:50]

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'


class Videos(models.Model):
    date_joined = models.DateField(default=datetime.now)
    title = models.CharField(max_length=250, verbose_name='Título')
    url = models.CharField(max_length=5000, verbose_name='Enlace')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.title

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        return item

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
