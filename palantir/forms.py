from django import forms
from django.forms import ModelForm

from .models import InformationSource, Specialist, VKDataSpecialist


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
    phone_number_information = forms.BooleanField(required=False, label='Phone number information')
    # instagram = forms.BooleanField(required=False, label='Instagram')
    # twitter = forms.BooleanField(required=False, label='Twitter')
    # pinterest = forms.BooleanField(required=False, label='Pinterest')

    class Meta:
        fields = ('vk', 'instagram', 'twitter',)


class InitialDataForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    # username = forms.CharField(max_length=100, required=False, label='Username')

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


class InitialDataPhoneNumberInformationForm(forms.Form):
    phone = forms.CharField(max_length=100, required=False, label='Номер телефона')

    class Meta:
        fields = ('phone',)


class VKDataSpecialistForm(ModelForm):
    class Meta:
        model = VKDataSpecialist
        fields = {
            'specialist',
            'vk_id',
            'domain',
            'bdate',
            'photo_200_orig',
            'photo_400_orig',
            'skype',
            'interests',
            'books',
            'tv',
            'quotes',
            'about',
            'games',
            'movies',
            'activities',
            'music',
            'site',
            'university_name',
            'faculty_name',
            'graduation',
            'education_form',
            'education_status',
            'home_town',
            'relation',
            'screen_name',
            'first_name',
            'last_name',
            'is_closed',
            'city',
            'country',
            'career',
            'military',
            'political',
            'universities',
            'schools',
            'number_of_friends',
            'visualization_of_friends_picture_name',
        }
        labels = {
            'specialist': 'Специалист',
            'vk_id': 'VK id',
            'domain': 'Короткий адрес страницы VK',
            'bdate': 'Дата рождения',
            'photo_200_orig': 'URL фотографии, имеющей ширину 200 пикселей',
            'photo_400_orig': 'URL фотографии, имеющей ширину 400 пикселей',
            'skype': 'Данные для связи в skype',
            'interests': 'Интересы',
            'books': 'Любимые книги',
            'tv': 'Любимые телешоу',
            'quotes': 'Любимые цитаты',
            'about': 'О себе',
            'games': 'Любимые игры',
            'movies': 'Любимые фильмы',
            'activities': 'Деятельность',
            'music': 'Любимая музыка',
            'site': 'Адрес сайта',
            'university_name': 'Наименование вуза',
            'faculty_name': 'Наименование факультета в вузе',
            'graduation': 'Год окончания обучения в вузе',
            'education_form': 'Форма обучения в вузе',
            'education_status': 'Статус в вузе',
            'home_town': 'Родной город',
            'relation': 'Семейное положение',
            'screen_name': 'Короткое имя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'is_closed': 'Закрыт ли аккаунт',
            'city': 'Город проживания',
            'country': 'Страна проживания',
            'career': 'Место работы',
            'military': 'Место военной службы',
            'political': 'Политические предпочтения',
            'universities': 'Список вузов',
            'schools': 'Список школ',
            'number_of_friends': 'Количество друзей',
            'visualization_of_friends_picture_name': 'Визуализация друзей',
        }
