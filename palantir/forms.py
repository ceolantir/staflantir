from django.forms import ModelForm
from django import forms

from .models import InformationSource, Specialist


class InformationSourceForm(ModelForm):
    class Meta:
        model = InformationSource
        fields = ('title', 'description')
        labels = {
            'title': 'Название информационного источника',
            'description': 'Описание информационного источника',
        }


class SpecialistForm(ModelForm):
    class Meta:
        model = Specialist
        fields = ('first_name', 'last_name', 'description')
        labels = {
            'first_name': 'Имя специалиста',
            'last_name': 'Фамилия специалиста',
            'description': 'Описание специалиста',
        }


class SearchForm(forms.Form):
    data = forms.CharField(
        max_length=30,
        label='Найти специалиста',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control w-100',
                'placeholder': 'Найти специалиста',
                'aria-label': 'Найти специалиста',
            },
        ))

    class Meta:
        fields = ('data',)
