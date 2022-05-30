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
    description = models.TextField(max_length=2000, verbose_name='Информация')
    image = models.ImageField(
        upload_to=MEDIA_SPECIALISTS_IMAGE_DIR,
        default=MEDIA_SPECIALISTS_IMAGE_DIR_default,
        verbose_name='Лого',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', default=User)

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
