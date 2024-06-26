from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from staflantir.settings import (
    MEDIA_INFORMATION_SOURCES_IMAGE_DIR,
    MEDIA_SPECIALISTS_IMAGE_DIR,
    MEDIA_SPECIALISTS_IMAGE_DIR_default,
    MEDIA_VK_DATA_IMAGE_DIR,
    MEDIA_VK_DATA_IMAGE_DIR_default,
)


class InformationSource(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Информация')
    image = models.ImageField(upload_to=MEDIA_INFORMATION_SOURCES_IMAGE_DIR, verbose_name='Лого')
    url = models.URLField(max_length=1000, null=True, blank=True, verbose_name='Ссылка на источник')

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


class VKInfo(models.Model):
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
    visualization_of_friends_default_picture_name = models.ImageField(
        upload_to=MEDIA_VK_DATA_IMAGE_DIR,
        default=MEDIA_VK_DATA_IMAGE_DIR_default,
        verbose_name='Визуализация друзей',
    )

    class Meta:
        verbose_name = 'Данные из VK'
        verbose_name_plural = 'Данные из VK'

    def __getitem__(self, key):
        return getattr(self, key)


class PhoneNumberInfo(models.Model):
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

    def __getitem__(self, key):
        return getattr(self, key)


class GitHubProfileInfo(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    name = models.CharField(max_length=100, verbose_name='Ник')
    public_repos = models.CharField(max_length=100, null=True, blank=True, verbose_name='Публичных репозиториев')
    followers = models.CharField(max_length=100, null=True, blank=True, verbose_name='Подписчиков')
    following = models.CharField(max_length=100, null=True, blank=True, verbose_name='Подписан')
    created_at = models.CharField(max_length=100, null=True, blank=True, verbose_name='Создан')
    updated_at = models.CharField(max_length=100, null=True, blank=True, verbose_name='Обновлен')
    company = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Компания')
    blog = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Блог')
    location = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Локация')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Почта')
    bio = models.CharField(max_length=1000, null=True, blank=True, verbose_name='О себе')
    twitter_username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ник в твиттере')

    class Meta:
        verbose_name = 'Данные из GitHub'
        verbose_name_plural = 'Данные из GitHub'

    def __getitem__(self, key):
        return getattr(self, key)


class GitHubReposInfo(models.Model):
    profile = models.ForeignKey(GitHubProfileInfo, on_delete=models.CASCADE, verbose_name='Профиль в Github')
    name = models.CharField(max_length=100, verbose_name='Название репозитория')
    language = models.CharField(max_length=100, null=True, blank=True, verbose_name='Язык программирования')
    visibility = models.CharField(max_length=100, null=True, blank=True, verbose_name='Публичный')
    archived = models.CharField(max_length=100, null=True, blank=True, verbose_name='Архивирован')
    fork = models.CharField(max_length=100, null=True, blank=True, verbose_name='Форкнут')
    created_at = models.CharField(max_length=100, null=True, blank=True, verbose_name='Создан')
    updated_at = models.CharField(max_length=100, null=True, blank=True, verbose_name='Обновлен')
    stargazers_count = models.CharField(max_length=100, null=True, blank=True, verbose_name='Количество звезд')
    forks = models.CharField(max_length=100, null=True, blank=True, verbose_name='Количество форков')
    contributors_info = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Контрибьюторы')

    class Meta:
        verbose_name = 'Данные репозиториев профиля из GitHub'
        verbose_name_plural = 'Данные репозиториев профилей из GitHub'

    def __getitem__(self, key):
        return getattr(self, key)


class SteamProfileInfo(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    name = models.CharField(max_length=100, verbose_name='Ник')
    created_at = models.CharField(max_length=50, null=True, blank=True, verbose_name='Создан')
    lvl = models.CharField(max_length=5, null=True, blank=True, verbose_name='Уровень')
    games_number = models.CharField(max_length=10, null=True, blank=True, verbose_name='Количество игр')
    total_hours = models.CharField(max_length=10, null=True, blank=True, verbose_name='Количество часов всего')

    class Meta:
        verbose_name = 'Данные из Steam'
        verbose_name_plural = 'Данные из Steam'

    def __getitem__(self, key):
        return getattr(self, key)


class SteamReposInfo(models.Model):
    profile = models.ForeignKey(SteamProfileInfo, on_delete=models.CASCADE, verbose_name='Профиль в Steam')
    name = models.CharField(max_length=100, verbose_name='Название игры')
    hours_forever = models.CharField(max_length=6, null=True, blank=True, verbose_name='Количество часов')

    class Meta:
        verbose_name = 'Данные игр профиля из Steam'
        verbose_name_plural = 'Данные игр профилей из Steam'

    def __getitem__(self, key):
        return getattr(self, key)


class HabrProfileInfo(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    name = models.CharField(max_length=100, verbose_name='Ник')
    rating_place = models.CharField(max_length=10, null=True, blank=True, verbose_name='Рейтинг')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='Откуда')
    job = models.CharField(max_length=100, null=True, blank=True, verbose_name='Работа')
    birthday = models.CharField(max_length=25, null=True, blank=True, verbose_name='Дата рождения')
    registered = models.CharField(max_length=25, null=True, blank=True, verbose_name='Зарегистрирован')

    class Meta:
        verbose_name = 'Данные из Habr'
        verbose_name_plural = 'Данные из Habr'

    def __getitem__(self, key):
        return getattr(self, key)


class HabrReposInfo(models.Model):
    profile = models.ForeignKey(HabrProfileInfo, on_delete=models.CASCADE, verbose_name='Профиль в Steam')
    url = models.CharField(max_length=1000, verbose_name='Ссылка на пост')
    rating = models.IntegerField(null=True, blank=True, verbose_name='Рейтинг поста')

    class Meta:
        verbose_name = 'Данные постов профиля из Habr'
        verbose_name_plural = 'Данные постов профилей из Habr'

    def __getitem__(self, key):
        return getattr(self, key)


class StackOverflowProfileInfo(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист')
    name = models.CharField(max_length=100, verbose_name='Ник')
    reputation = models.IntegerField(null=True, blank=True, verbose_name='Репутация')
    affected = models.IntegerField(null=True, blank=True, verbose_name='Примерное число раз, когда посетители видели полезные сообщения')
    answers = models.IntegerField(null=True, blank=True, verbose_name='Количество данных ответов')
    questions = models.IntegerField(null=True, blank=True, verbose_name='Количество заданных вопросов')

    class Meta:
        verbose_name = 'Данные из StackOverflow'
        verbose_name_plural = 'Данные из StackOverflow'

    def __getitem__(self, key):
        return getattr(self, key)
