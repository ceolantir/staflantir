from django.contrib import admin

from .models import (
    InformationSource,
    Specialist,
    VKDataSpecialist,
    PhoneNumberInformationSpecialist,
)


@admin.register(InformationSource)
class InformationSourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
    )
    list_display_links = ('title',)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
    )
    list_display_links = ('first_name', 'last_name',)


@admin.register(VKDataSpecialist)
class VKDataSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'first_name',
        'last_name',
    )
    list_display_links = ('specialist', 'first_name', 'last_name',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(PhoneNumberInformationSpecialist)
class PhoneNumberInformationSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'phone'
    )
    list_display_links = ('specialist', 'phone',)
    list_filter = ('specialist', 'specialist__owner',)
