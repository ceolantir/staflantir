from django.contrib import admin

from .models import InformationSource, Specialist


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
        'description',
    )
    list_display_links = ('first_name', 'last_name',)
