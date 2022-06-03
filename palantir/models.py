from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from staflantir.settings import (
    MEDIA_INFORMATION_SOURCES_IMAGE_DIR,
    MEDIA_SPECIALISTS_IMAGE_DIR,
    MEDIA_SPECIALISTS_IMAGE_DIR_default,
)


class InformationSource(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Информация')
    image = models.ImageField(upload_to=MEDIA_INFORMATION_SOURCES_IMAGE_DIR, verbose_name='Лого')

    class Meta:
        verbose_name = 'Информационный источник'
        verbose_name_plural = 'Информационные источники'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_information_source', kwargs={'pk': self.pk})


class Specialist(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание специалиста')
    image = models.ImageField(
        upload_to=MEDIA_SPECIALISTS_IMAGE_DIR,
        default=MEDIA_SPECIALISTS_IMAGE_DIR_default,
        verbose_name='Лого',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=User, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('specialists', kwargs={'pk': self.pk})

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    def full_name_2(self):
        return f'{self.first_name} {self.last_name}'


class VKDataSpecialist(models.Model):
    information_source = models.ForeignKey(InformationSource, on_delete=models.CASCADE, verbose_name='Информационный источник')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Фамилия')
    bdate = models.CharField(max_length=100, null=True, blank=True, verbose_name='Дата рождения')
    number_of_friends = models.CharField(max_length=100, null=True, blank=True, verbose_name='Количество друзей')
    home_town = models.CharField(max_length=100, null=True, blank=True, verbose_name='Родной город')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город проживания')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна проживания')
    relation = models.CharField(max_length=100, null=True, blank=True, verbose_name='Семейное положение')
    screen_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Короткое имя')
    vk_id = models.CharField(max_length=100, verbose_name='VK id')
    domain = models.CharField(max_length=100, null=True, blank=True, verbose_name='Короткий адрес страницы VK')
    skype = models.CharField(max_length=100, null=True, blank=True, verbose_name='Данные для связи в skype')
    schools = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Список школ')
    universities = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Список вузов')
    career = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Место работы')
    military = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Место военной службы')
    interests = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Интересы')
    books = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимые книги')
    tv = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимые телешоу')
    quotes = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимые цитаты')
    about = models.CharField(max_length=1000, null=True, blank=True, verbose_name='О себе')
    games = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимые игры')
    movies = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимые фильмы')
    activities = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Деятельность')
    music = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Любимая музыка')
    site = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Адрес сайта')
    political = models.CharField(max_length=100, null=True, blank=True, verbose_name='Политические предпочтения')
    university_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Наименование вуза')
    faculty_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Наименование факультета в вузе')
    graduation = models.CharField(max_length=100, null=True, blank=True, verbose_name='Год окончания обучения в вузе')
    education_form = models.CharField(max_length=100, null=True, blank=True, verbose_name='Форма обучения в вузе')
    education_status = models.CharField(max_length=100, null=True, blank=True, verbose_name='Статус в вузе')
    is_closed = models.CharField(max_length=100, null=True, blank=True, verbose_name='Закрыт ли аккаунт')
    photo_200_orig = models.CharField(max_length=1000, null=True, blank=True, verbose_name='URL фотографии, имеющей ширину 200 пикселей')
    photo_400_orig = models.CharField(max_length=1000, null=True, blank=True, verbose_name='URL фотографии, имеющей ширину 400 пикселей')
    visualization_of_friends_picture_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Визуализация друзей')

    class Meta:
        verbose_name = 'Данные из VK'
        verbose_name_plural = 'Данные из VK'

    def __getitem__(self, key):
        return getattr(self, key)


class PhoneNumberInformationSpecialist(models.Model):
    information_source = models.ForeignKey(InformationSource, on_delete=models.CASCADE, verbose_name='Информационный источник')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    phone = models.IntegerField(verbose_name='Номер телефона')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')
    okrug = models.CharField(max_length=100, null=True, blank=True, verbose_name='Округ')
    region = models.CharField(max_length=100, null=True, blank=True, verbose_name='Регион')
    time_zone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Временная зона')
    oper_brand = models.CharField(max_length=100, null=True, blank=True, verbose_name='Мобильный оператор')

    class Meta:
        verbose_name = 'Данные номера телефона'
        verbose_name_plural = 'Данные номеров телефонов'
