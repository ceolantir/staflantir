from django.contrib import admin

from .models import (
    InformationSource,
    Specialist,
    VKInfo,
    PhoneNumberInfo,
    GitHubProfileInfo,
    GitHubReposInfo,
    SteamProfileInfo,
    SteamReposInfo,
    HabrProfileInfo,
    HabrReposInfo,
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


@admin.register(VKInfo)
class VKInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'first_name',
        'last_name',
    )
    list_display_links = ('specialist', 'first_name', 'last_name',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(PhoneNumberInfo)
class PhoneNumberInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'phone'
    )
    list_display_links = ('specialist', 'phone',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(GitHubProfileInfo)
class GitHubProfileInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'name'
    )
    list_display_links = ('specialist', 'name',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(GitHubReposInfo)
class GitHubReposInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'name',
    )
    list_display_links = ('profile', 'name',)
    list_filter = ('profile', 'profile__specialist', 'profile__specialist__owner',)


@admin.register(SteamProfileInfo)
class SteamProfileInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'name'
    )
    list_display_links = ('specialist', 'name',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(SteamReposInfo)
class SteamReposInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'name',
    )
    list_display_links = ('profile', 'name',)
    list_filter = ('profile', 'profile__specialist', 'profile__specialist__owner',)


@admin.register(HabrProfileInfo)
class HabrProfileInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'specialist',
        'name'
    )
    list_display_links = ('specialist', 'name',)
    list_filter = ('specialist', 'specialist__owner',)


@admin.register(HabrReposInfo)
class HabrReposInfoSpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'url',
    )
    list_display_links = ('profile', 'url',)
    list_filter = ('profile', 'profile__specialist', 'profile__specialist__owner',)
    ordering = ('rating',)