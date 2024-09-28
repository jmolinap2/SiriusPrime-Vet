import json
import os
import random
import string
from datetime import date
from os.path import basename

import django
from django.core.files import File
from django.core.management import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group
from core.clinic.models import *


class Command(BaseCommand):
    help = "It allows me to insert test data into the software"

    def handle(self, *args, **options):
        numbers = list(string.digits)
        numbers_letters = list(string.digits) + list(string.ascii_uppercase)

        company = Company.objects.create(
            name='Sirius Prime',
            ruc='0928363993001',
            proprietor='Jesús Alejandro Molina P.',
            description='Somos una clínica veterinaria enfocada en la atención integral de las mascotas, convencidos en que toda mascota merece una atención de alta calidad y calidez, con médicos especializados, equipos de diagnóstico y protocolos actualizados, cuidamos de la salud y bienestar de las mascotas',
            with_us='Somos una clínica veterinaria que se dedica a la prestación de un servicio integral en los ámbitos de los cuidados clínicos veterinarios y asesoramiento.',
            mission='Ofrecer bienestar tanto animal, como a las familias de nuestros pacientes a través de la prestación de servicios médicos veterinarios y complementarios, entregando calidad y satisfacción, superando las expectativas de nuestros clientes, contribuyendo a la innovación y desarrollo profesional del sector Médico Veterinario de la Región.',
            vision='Buscar la excelencia en la prevención, detección y curación de enfermedades en animales de compañía, aumentando el nivel de seguridad sanitaria en quienes conviven con ellos y hacerlo de forma sostenible, rentable, profesional y ética; así como mejorar la relación afectiva entre las mascotas y sus propietarios, generando un mayor equilibrio sanitario y emocional en ambos.',
            about_us='Contribuir y satisfacer las necesidades de nuestros clientes ofreciendo un servicio rápido, garantizando altos estándares de calidad diagnóstica.',
            phone='2977557',
            mobile='0979014551',
            email='williamjair94@hotmail.com',
            address='Carlos, Julio Arosemena monroy, Milagro',
            horary='Lunes a Sábado de 08:00 a 21:00',
            latitude='-2.1436557',
            longitude='-79.5985745',
            about_youtube='https://youtu.be/znjbyrslLDw',
            iva=12.00
        )
        image_path = f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/logo.png'
        company.image.save(basename(image_path), content=File(open(image_path, 'rb')), save=False)
        company.save()

        with open(f'{settings.BASE_DIR}/deploy/json/countries.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                Country.objects.get_or_create(code=item['id'], name=item['name'])

        country = Country.objects.get(name='Ecuador')
        with open(f'{settings.BASE_DIR}/deploy/json/provinces.json', encoding='utf8') as json_file:
            data = json.load(json_file)
            for id_province, object_province in data.items():
                if 'provincia' in object_province:
                    province = Province.objects.get_or_create(country=country, code=id_province, name=object_province['provincia'])[0]
                    for id_canton, object_canton in object_province['cantones'].items():
                        canton = Canton.objects.get_or_create(province=province, name=object_canton['canton'])[0]
                        for id_parish, object_parish in object_canton['parroquias'].items():
                            Parish.objects.get_or_create(canton=canton, name=object_parish)

        for name in ['Medicina Veterinaria', 'Zootecnia', 'Biología Marina', 'Medicina alternativa']:
            Profession.objects.create(name=name)

        with open(f'{settings.BASE_DIR}/deploy/json/colors.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                Color.objects.get_or_create(name=item['name'], hex=item['hex'])

        for name in ['Gato', 'Perro']:
            TypePet.objects.create(name=name)

        type_pet_id = list(TypePet.objects.filter().values_list('id', flat=True))
        with open(f'{settings.BASE_DIR}/deploy/json/breed.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                BreedPet.objects.create(name=item['name'], type_pet_id=random.choice(type_pet_id))

        with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                SubCategory.objects.get_or_create(name=item['form'])

        subcategory_id = list(SubCategory.objects.filter().values_list('id', flat=True))
        with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                Category.objects.get_or_create(name=item['brandName'])
            for category in Category.objects.all():
                for i in random.choices(subcategory_id, k=4):
                    category.sub_category.add(SubCategory.objects.get(pk=i))

        with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
            data = json.load(json_file)
            for item in data[0:15]:
                provider = Provider.objects.create(
                    name=item['company'].upper(),
                    ruc=''.join(random.choices(numbers, k=13)),
                    mobile=''.join(random.choices(numbers, k=10)),
                    address=item['country'],
                    email=item['email']
                )
                print(f'Record inserted provider {provider.id}')

            parish_id = list(Parish.objects.filter().values_list('id', flat=True))
            group = Group.objects.get(pk=settings.GROUPS['client'])

            for item in data[16:30]:
                dni = ''.join(random.choices(numbers, k=10))
                user = User.objects.create(
                    names=f"{item['first']} {item['last']}",
                    email=item['email'],
                    username=dni
                )
                user.set_password(user.username)
                user.groups.add(group)
                user.save()

                Client.objects.create(
                    user=user,
                    dni=dni,
                    birthdate=date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28)),
                    mobile=''.join(random.choices(numbers, k=10)),
                    phone=''.join(random.choices(numbers, k=7)),
                    address=item['country'],
                    parish_id=random.choice(parish_id)
                )

            group = Group.objects.get(pk=settings.GROUPS['employee'])
            profession_id = list(Profession.objects.filter().values_list('id', flat=True))

            for item in data[31:45]:
                dni = ''.join(random.choices(numbers, k=10))
                user = User.objects.create(
                    names=f"{item['first']} {item['last']}",
                    email=item['email'],
                    username=dni
                )
                user.set_password(user.username)
                user.groups.add(group)
                user.save()

                Employee.objects.create(
                    user=user,
                    dni=dni,
                    birthdate=date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28)),
                    mobile=''.join(random.choices(numbers, k=10)),
                    phone=''.join(random.choices(numbers, k=7)),
                    address=item['country'],
                    parish_id=random.choice(parish_id),
                    profession_id=random.choice(profession_id)
                )

            category_id = list(Category.objects.values_list('id', flat=True))

            with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
                product_data = json.load(json_file)[0:30]
                for item in product_data:
                    product = Product.objects.create(
                        name=item['genericName'],
                        code=''.join(random.choices(numbers_letters, k=8)),
                        type=random.choices(PRODUCT_TYPE, k=1)[0][0],
                        category_id=random.choice(category_id),
                        price=random.randint(5, 30)
                    )
                    product.pvp = product.price + product.price * 0.20
                    product.save()
                    print(f'record inserted product {product.id}')

            provider_id = list(Provider.objects.values_list('id', flat=True))
            product_id = list(Product.objects.values_list('id', flat=True))

            for i in range(1, 10):
                purchase = Purchase.objects.create(
                    number=''.join(random.choices(numbers, k=8)),
                    provider_id=random.choice(provider_id)
                )
                print(f'record inserted purchase {purchase.id}')

                for d in range(1, 5):
                    product = Product.objects.get(id=random.choice(product_id))
                    cant = random.randint(1, 10)
                    detail = PurchaseDetail.objects.create(
                        purchase_id=purchase.id,
                        product_id=product.id,
                        cant=cant,
                        price=product.pvp,
                        subtotal=float(product.pvp) * cant
                    )

                    while PurchaseDetail.objects.filter(purchase_id=purchase.id, product_id=detail.product_id).exclude(id=detail.id).exists():
                        detail.product_id = random.choice(product_id)

                    detail.save()
                    detail.product.stock += detail.cant
                    detail.product.save()

                purchase.calculate_invoice()

        client_id = list(Client.objects.values_list('id', flat=True))
        color_id = list(Color.objects.values_list('id', flat=True))
        breed_pet_id = list(BreedPet.objects.values_list('id', flat=True))

        with open(f'{settings.BASE_DIR}/deploy/json/mascots.json', encoding='utf8') as json_file:
            mascot_data = json.load(json_file)
            for item in mascot_data:
                Mascot.objects.create(
                    name=item,
                    client_id=random.choice(client_id),
                    color_id=random.choice(color_id),
                    breed_pet_id=random.choice(breed_pet_id),
                    gender=GENDER_PET[0][0] if random.randint(1, 2) == 1 else GENDER_PET[1][0],
                    birthdate=date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28))
                )

        for name in ['Respiración', 'Presión arterial', 'Pulso', 'Temperatura', 'Peso']:
            MedicalParameter.objects.create(name=name)
