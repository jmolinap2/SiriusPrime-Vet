import os
from os.path import basename

import django
from django.core.files import File
from django.core.management import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.security.models import *
from core.clinic.models import *
from core.homepage.models import *
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = "Allows to initiate the base software installation"

    def handle(self, *args, **options):
        dashboard = Dashboard.objects.create(
            name='PEGASUS',
            author='William Jair Dávila Vargas',
            icon='fas fa-paw',
            layout=1,
            navbar='navbar-dark navbar-navy',
            sidebar='sidebar-dark-navy'
        )
        image_path = f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/logo.png'
        dashboard.image.save(basename(image_path), content=File(open(image_path, 'rb')), save=False)
        dashboard.save()

        moduletype = ModuleType.objects.create(name='Seguridad', icon='fas fa-lock')
        print(f'insertado {moduletype.name}')

        modules_data = [
            {
                'name': 'Tipos de Módulos',
                'url': '/security/module/type/',
                'icon': 'fas fa-door-open',
                'description': 'Permite administrar los tipos de módulos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Módulos',
                'url': '/security/module/',
                'icon': 'fas fa-th-large',
                'description': 'Permite administrar los módulos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Grupos',
                'url': '/security/group/',
                'icon': 'fas fa-users',
                'description': 'Permite administrar los grupos de usuarios del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Respaldos',
                'url': '/security/database/backups/',
                'icon': 'fas fa-database',
                'description': 'Permite administrar los respaldos de base de datos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Conf. Dashboard',
                'url': '/security/dashboard/update/',
                'icon': 'fas fa-tools',
                'description': 'Permite configurar los datos de la plantilla',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Dashboard._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Accesos',
                'url': '/security/user/access/',
                'icon': 'fas fa-user-secret',
                'description': 'Permite administrar los accesos de los usuarios',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=UserAccess._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Usuarios',
                'url': '/user/',
                'icon': 'fas fa-user',
                'description': 'Permite administrar a los administradores del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Cambiar password',
                'url': '/user/update/password/',
                'icon': 'fas fa-key',
                'description': 'Permite cambiar tu password de tu cuenta',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Editar perfil',
                'url': '/user/update/profile/',
                'icon': 'fas fa-user',
                'description': 'Permite cambiar la información de tu cuenta',
                'moduletype': None,
                'permissions': None
            }
        ]

        moduletype = ModuleType.objects.create(name='Bodega', icon='fas fa-boxes')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Proveedores',
                'url': '/clinic/provider/',
                'icon': 'fas fa-truck-loading',
                'description': 'Permite administrar a los proveedores para las compras',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'SubCategorías',
                'url': '/clinic/sub/category/',
                'icon': 'fab fa-linode',
                'description': 'Permite administrar las subcategorías de los productos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=SubCategory._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Categorías',
                'url': '/clinic/category/',
                'icon': 'fab fa-linode',
                'description': 'Permite administrar las categorías de los productos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Compras',
                'url': '/clinic/purchase/',
                'icon': 'fas fa-vote-yea',
                'description': 'Permite administrar las compras del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Productos',
                'url': '/clinic/product/',
                'icon': 'fas fa-box-open',
                'description': 'Permite administrar los productos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()))
            }
        ])

        moduletype = ModuleType.objects.create(name='Página Web', icon='fas fa-house-damage')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Noticias',
                'url': '/news/',
                'icon': 'far fa-newspaper',
                'description': 'Permite administrar las noticias del dashboard',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=News._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Videos',
                'url': '/videos/',
                'icon': 'fas fa-photo-video',
                'description': 'Permite administrar las videos del dashboard',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Videos._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Redes Sociales',
                'url': '/social/networks/',
                'icon': 'far fa-thumbs-up',
                'description': 'Permite administrar las redes sociales de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=SocialNetworks._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Departamentos',
                'url': '/departments/',
                'icon': 'fas fa-city',
                'description': 'Permite administrar los departamentos de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Departments._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Servicios',
                'url': '/services/',
                'icon': 'fas fa-atlas',
                'description': 'Permite administrar los servicios de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Services._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Estadísticas',
                'url': '/statistics/',
                'icon': 'fab fa-stack-overflow',
                'description': 'Permite administrar las estadísticas de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Statistics._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Preguntas frecuentes',
                'url': '/frequent/questions/',
                'icon': 'fas fa-question-circle',
                'description': 'Permite administrar las preguntas frecuentes de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=FrequentQuestions._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Testimonios',
                'url': '/testimonials/',
                'icon': 'fas fa-comment-alt',
                'description': 'Permite administrar los testimonios de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Testimonials._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Galería',
                'url': '/gallery/',
                'icon': 'fas fa-file-image',
                'description': 'Permite administrar las imágenes de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Gallery._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Doctores',
                'url': '/team/',
                'icon': 'fas fa-users-cog',
                'description': 'Permite administrar a los doctores de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Team._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Comentarios',
                'url': '/comments/',
                'icon': 'fas fa-envelope',
                'description': 'Permite administrar los comentarios de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Comments._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Cualidades',
                'url': '/qualities/',
                'icon': 'fas fa-folder-open',
                'description': 'Permite administrar los comentarios de la página',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Qualities._meta.label.split('.')[1].lower()))
            }
        ])

        moduletype = ModuleType.objects.create(name='Ubicación', icon='fas fa-street-view')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Paises',
                'url': '/clinic/country/',
                'icon': 'fas fa-globe-europe',
                'description': 'Permite administrar los paises',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Country._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Provincias',
                'url': '/clinic/province/',
                'icon': 'fas fa-globe',
                'description': 'Permite administrar las provincias del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Province._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Cantones',
                'url': '/clinic/canton/',
                'icon': 'fas fa-globe-americas',
                'description': 'Permite administrar los cantones del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Canton._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Parroquias',
                'url': '/clinic/parish/',
                'icon': 'fas fa-search-location',
                'description': 'Permite administrar las parroquias del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Parish._meta.label.split('.')[1].lower()))
            }
        ])

        moduletype = ModuleType.objects.create(name='Veterinaria', icon='fas fa-hospital')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Compañia',
                'url': '/clinic/company/update/',
                'icon': 'fas fa-home',
                'description': 'Permite administrar la información de la empresa',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Company._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Empleados',
                'url': '/clinic/employee/',
                'icon': 'fas fa-male',
                'description': 'Permite administrar a los empleados del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Employee._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Profesiones',
                'url': '/clinic/profession/',
                'icon': 'fas fa-user-md',
                'description': 'Permite administrar las profesiones de los empleados',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Profession._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Clientes',
                'url': '/clinic/client/',
                'icon': 'fas fa-male',
                'description': 'Permite administrar a los clientes del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Mascotas',
                'url': '/clinic/mascot/',
                'icon': 'fas fa-bone',
                'description': 'Permite administrar las mascotas del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(codename__in=['view_mascot', 'add_mascot', 'change_mascot', 'delete_mascot']))
            },
            {
                'name': 'Colores',
                'url': '/clinic/color/',
                'icon': 'fas fa-file-medical',
                'description': 'Permite administrar los colores del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Color._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Tipos de Animales',
                'url': '/clinic/type/pet/',
                'icon': 'fas fa-folder',
                'description': 'Permite administrar a los tipos de animales del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=TypePet._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Razas de Animales',
                'url': '/clinic/breed/pet/',
                'icon': 'fas fa-folder-open',
                'description': 'Permite administrar las razas de las mascotas del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=BreedPet._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Parámetros Médicos',
                'url': '/clinic/medical/parameter/',
                'icon': 'fas fa-mortar-pestle',
                'description': 'Permite administrar los parámetros médicos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=MedicalParameter._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Historial de Vacunas',
                'url': '/clinic/pet/history/vaccines/',
                'icon': 'fas fa-first-aid',
                'description': 'Permite administrar los historiales de las vacunas',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Historial Médico',
                'url': '/clinic/pet/history/medical/',
                'icon': 'fas fa-calendar-alt',
                'description': 'Permite administrar los historiales médicos de la mascota',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Ventas y Citas Med.',
                'url': '/clinic/sale/',
                'icon': 'fas fa-shopping-cart',
                'description': 'Permite administrar las ventas de la veterinaria',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(codename__in=['view_sale', 'delete_sale']))
            }
        ])

        moduletype = ModuleType.objects.create(name='Reportes', icon='fas fa-chart-pie')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Reporte de Ganancias',
                'url': '/reports/earnings/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las ganancias de los productos',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Reporte de Ventas',
                'url': '/reports/sale/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las ventas',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Reporte de Compras',
                'url': '/reports/purchase/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las compras',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Reporte de Clientes',
                'url': '/reports/client/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de los clientes',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Reporte de Mascotas',
                'url': '/reports/mascot/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las mascotas',
                'moduletype': moduletype,
                'permissions': None
            }
        ])

        modules_data.extend([
            {
                'name': 'Mascotas',
                'url': '/clinic/mascot/client/',
                'icon': 'fas fa-bone',
                'description': 'Permite administrar las mascotas del sistema',
                'moduletype': None,
                'permissions': list(Permission.objects.filter(codename__in=['view_mascot_client', 'add_mascot_client', 'change_mascot_client', 'delete_mascot_client']))
            },
            {
                'name': 'Historial de Vacunas',
                'url': '/clinic/pet/history/client/vaccines/',
                'icon': 'fas fa-first-aid',
                'description': 'Permite administrar los historiales de las vacunas',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Historial Médico',
                'url': '/clinic/pet/history/client/medical/',
                'icon': 'fas fa-calendar-alt',
                'description': 'Permite administrar los historiales médicos de la mascota',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Editar perfil',
                'url': '/clinic/client/update/profile/',
                'icon': 'fas fa-user',
                'description': 'Permite cambiar la información de tu cuenta',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Ventas y Citas Med.',
                'url': '/clinic/sale/employee/',
                'icon': 'fas fa-shopping-cart',
                'description': 'Permite administrar las ventas de la veterinaria',
                'moduletype': None,
                'permissions': list(Permission.objects.filter(codename__in=['view_sale_employee', 'add_sale_employee', 'delete_sale_employee', 'attend_sale_employee']))
            },
            {
                'name': 'Ventas y Citas Med.',
                'url': '/clinic/sale/client/',
                'icon': 'fas fa-shopping-cart',
                'description': 'Permite administrar las ventas de la veterinaria',
                'moduletype': None,
                'permissions': list(Permission.objects.filter(codename__in=['view_sale_client', 'add_sale_client']))
            }
        ])

        for module_data in modules_data:
            module = Module.objects.create(
                module_type=module_data['moduletype'],
                name=module_data['name'],
                url=module_data['url'],
                icon=module_data['icon'],
                description=module_data['description']
            )
            if module_data['permissions']:
                for permission in module_data['permissions']:
                    module.permissions.add(permission)
            print(f'insertado {module.name}')

        CLIENT_URLS = [
            '/clinic/sale/client/',
            '/clinic/client/update/profile/',
            '/clinic/pet/history/client/medical/',
            '/clinic/pet/history/client/vaccines/',
            '/clinic/mascot/client/'
        ]

        EMPLOYEE_URLS = [
            '/clinic/employee/update/profile/',
            '/clinic/sale/employee/'
        ]

        group = Group.objects.create(name='Administrador')
        print(f'insertado {group.name}')

        for module in Module.objects.filter().exclude(url__in=CLIENT_URLS + EMPLOYEE_URLS):
            GroupModule.objects.create(module=module, group=group)
            for permission in module.permissions.all():
                group.permissions.add(permission)

        user = User.objects.create(
            names='William Jair Dávila Vargas',
            username='admin',
            email='davilawilliam93@gmail.com',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        user.set_password('hacker94')
        user.save()
        user.groups.add(group)
        print(f'Bienvenido {user.names}')

        group = Group.objects.create(name='Cliente')
        print(f'insertado {group.name}')

        for module in Module.objects.filter(url__in=CLIENT_URLS + ['/user/update/password/']):
            GroupModule.objects.create(module=module, group=group)
            for permission in module.permissions.all():
                group.permissions.add(permission)

        group = Group.objects.create(name='Empleado')
        print(f'insertado {group.name}')

        for module in Module.objects.filter(url__in=EMPLOYEE_URLS + ['/user/update/password/', '/clinic/mascot/', '/clinic/pet/history/medical/', '/clinic/pet/history/vaccines/']):
            GroupModule.objects.create(module=module, group=group)
            for permission in module.permissions.all():
                group.permissions.add(permission)
