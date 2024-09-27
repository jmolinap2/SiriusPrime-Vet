from datetime import datetime

from django import forms

from core.clinic.choices import *
from core.clinic.models import Mascot, Category, BreedPet, Product
from core.reports.choices import MONTHS


class ReportForm(forms.Form):
    year = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#year',
    }), label='Año')

    month = forms.ChoiceField(choices=MONTHS, widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }), label='Mes')

    date_joined = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#date_joined'
        }), label='Fecha de registro')

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rangos de fecha')

    start_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'start_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#start_date'
        }), label='Fecha de inicio')

    end_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'end_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#end_date'
        }), label='Fecha de finalización')

    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese una descripción para buscar',
        'autocomplete': 'off'
    }), label='Buscador')

    mascot = forms.ModelChoiceField(queryset=Mascot.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }), label='Mascotas')

    type_sale = forms.ChoiceField(choices=TYPE_SALE, widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }), label='Tipo de venta')

    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }), label='Categoría')

    product = forms.ModelChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'form-control select2',
        'multiple': 'multiple'
    }), queryset=Product.objects.all(), label='Productos')

    breed_pet = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }), queryset=BreedPet.objects.all(), label='Tipo de raza')
