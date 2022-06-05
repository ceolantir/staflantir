from django import forms
from django.forms import ModelForm

from .models import InformationSource, Specialist, VKInfo


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


class InformationSourcesSelectionForm(forms.Form):
    vk = forms.BooleanField(required=False, label='VK')
    phone_number_information = forms.BooleanField(required=False, label='Phone number')
    github = forms.BooleanField(required=False, label='GitHub')
    steam = forms.BooleanField(required=False, label='Steam')
    habr = forms.BooleanField(required=False, label='Habr')
    stackoverflow = forms.BooleanField(required=False, label='StackOverflow')
    # instagram = forms.BooleanField(required=False, label='Instagram')
    # twitter = forms.BooleanField(required=False, label='Twitter')
    # pinterest = forms.BooleanField(required=False, label='Pinterest')

    class Meta:
        fields = ('vk', 'phone_number_information', 'github',)


class InitialDataForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    class Meta:
        fields = ('first_name', 'last_name',)


class InitialDataVKForm(forms.Form):
    user_id_vk = forms.CharField(max_length=100, label='ID в VK')
    visualization_friends = forms.BooleanField(
        required=False,
        label='Необходимость в визуализации друзей. '
              'Требуемое время коррелирует с количеством друзей в VK у специалиста. '
              'При небольшом количестве друзей ценность в визуализации крайне мала.',
    )

    class Meta:
        fields = ('first_name', 'last_name', 'user_id_vk',)


class InitialDataPhoneNumberInfoForm(forms.Form):
    phone = forms.IntegerField(max_value=79999999999, min_value=70000000000, label='Номер телефона')

    class Meta:
        fields = ('phone',)


class InitialDataGitHubForm(forms.Form):
    github_nickname = forms.CharField(max_length=100, label='Ник в GitHub')

    class Meta:
        fields = ('github_nickname',)


class InitialDataSteamForm(forms.Form):
    steam_nickname = forms.CharField(max_length=100, label='Ник в Steam')

    class Meta:
        fields = ('steam_nickname',)


class InitialDataHabrForm(forms.Form):
    habr_nickname = forms.CharField(max_length=100, label='Ник в Habr')

    class Meta:
        fields = ('habr_nickname',)


class InitialDataStackOverflowForm(forms.Form):
    stackoverflow_nickname = forms.CharField(max_length=100, label='Ник в StackOverflow')

    class Meta:
        fields = ('stackoverflow_nickname',)
