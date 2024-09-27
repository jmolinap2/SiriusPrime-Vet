from django import forms

from core.homepage.models import *


class SocialNetworksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['css'].widget.attrs['autofocus'] = True

    class Meta:
        model = SocialNetworks
        fields = '__all__'
        widgets = {
            'css': forms.TextInput(attrs={'placeholder': 'Ingrese una clase css'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ingrese un icono font-awesome'}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class DepartmentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departments
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un titulo'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class StatisticsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Statistics
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'cant': forms.TextInput(),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class FrequentQuestionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['autofocus'] = True

    class Meta:
        model = FrequentQuestions
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Ingrese una pregunta', 'rows': 4, 'cols': 4}),
            'answer': forms.Textarea(attrs={'placeholder': 'Ingrese una respuesta', 'rows': 4, 'cols': 4}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestimonialsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Testimonials
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'job': forms.TextInput(attrs={'placeholder': 'Ingrese un cargo'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese un comentario', 'rows': 3, 'cols': 3}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GalleryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'job': forms.TextInput(attrs={
                'placeholder': 'Ingrese un cargo',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'phrase': forms.TextInput(attrs={
                'placeholder': 'Ingrese una frase',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'class': 'form-control',
                'autocomplete': 'off',
                'rows': 3,
                'cols': 3,
            }),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un número de teléfono'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 4, 'cols': 4}),
        }


class QualitiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Qualities
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['autofocus'] = True

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un título'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'cols': 5, 'rows': 5}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese un enlace web'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class VideosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus'] = True

    class Meta:
        model = Videos
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese una url'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control-checkbox'})
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data
