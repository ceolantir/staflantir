from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value as V, Q
from django.db.models.functions import Concat
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View

from . import constants
from .discovery.github.github import GitHub
from .discovery.habr.habr import Habr
from .discovery.phone_number.search_phone_info import PhoneNumber
from .discovery.stackoverflow.stackoverflow import StackOverflow
from .discovery.steam.steam import Steam
from .discovery.vk.vk import VK
from .forms import (
    SearchForm,
    InformationSourcesSelectionForm,
    InitialDataForm,
    InitialDataVKForm,
    SpecialistForm,
    InitialDataPhoneNumberInfoForm,
    InitialDataGitHubForm,
    InitialDataSteamForm,
    InitialDataHabrForm,
    InitialDataStackOverflowForm,
)
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
    StackOverflowProfileInfo,
)


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['information_sources'] = InformationSource.objects.all().order_by('title')
        context['form'] = SearchForm

        return context


class DetailInformationSourceView(TemplateView):
    template_name = 'information_sources/detail_information_source.html'

    def get_context_data(self, **kwargs):
        context = super(DetailInformationSourceView, self).get_context_data(**kwargs)
        context['information_source'] = get_object_or_404(InformationSource, pk=kwargs['pk'])

        return context


class SpecialistsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'specialists/all_specialists.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialistsView, self).get_context_data(**kwargs)
        context['specialists'] = Specialist.objects.all().filter(
            Q(owner=self.request.user),
        ).order_by('last_name')
        context['form'] = SearchForm

        return context


class DetailSpecialistView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'specialists/detail_specialist.html'

    def get_context_data(self, **kwargs):
        context = super(DetailSpecialistView, self).get_context_data(**kwargs)
        context['specialist'] = get_object_or_404(
            Specialist,
            pk=kwargs['pk'],
            owner=self.request.user,
        )

        specialist_vk = VKInfo.objects.all().filter(Q(specialist=context['specialist']))
        if specialist_vk:
            context['specialist_data_vk'] = specialist_vk[0]
            context['specialist_data_vk_fields'] = {}

            for field in context['specialist_data_vk']._meta.get_fields():
                key = str(field).split('.')[-1]
                value = context['specialist_data_vk'][key]

                if not value or key in constants.attribute_exceptions_vk_data_specialist:
                    continue
                if key == 'is_closed' and value == 'Закрыт':
                    continue

                context['specialist_data_vk_fields'][field.verbose_name] = value

        specialist_data_phone = PhoneNumberInfo.objects.all().filter(
            Q(specialist=context['specialist']),
        )
        if specialist_data_phone:
            context['specialist_phone_number'] = specialist_data_phone[0]
            context['specialist_phone_number_fields'] = {}

            for field in context['specialist_phone_number']._meta.get_fields():
                key = str(field).split('.')[-1]
                if key in ('id', 'specialist'):
                    continue

                value = context['specialist_phone_number'][key]

                context['specialist_phone_number_fields'][field.verbose_name] = value

        specialist_github_profile_info = GitHubProfileInfo.objects.all().filter(
            Q(specialist=context['specialist']),
        )
        if specialist_github_profile_info:
            context['specialist_github_profile_info'] = specialist_github_profile_info[0]
            context['specialist_github_profile_info_fields'] = {}

            for field in context['specialist_github_profile_info']._meta.get_fields():
                key = str(field).split('.')[-1]
                if key in ('githubreposinfo>', 'id', 'specialist'):
                    continue

                value = context['specialist_github_profile_info'][key]
                if value is None:
                    continue

                context['specialist_github_profile_info_fields'][field.verbose_name] = value

            specialist_github_repos_objects = GitHubReposInfo.objects.all().filter(
                Q(profile=context['specialist_github_profile_info']),
            )
            specialist_github_repos_info_fields = []

            for specialist_github_repo_info in specialist_github_repos_objects:
                specialist_github_repo_info_fields = {}

                for field in specialist_github_repo_info._meta.get_fields():
                    key = str(field).split('.')[-1]
                    if key in ('id', 'profile'):
                        continue

                    value = specialist_github_repo_info[key]
                    if value is None:
                        continue

                    specialist_github_repo_info_fields[field.verbose_name] = value

                specialist_github_repos_info_fields.append(specialist_github_repo_info_fields)

            context['specialist_github_repos_info_fields'] = specialist_github_repos_info_fields

        specialist_steam_profile_info = SteamProfileInfo.objects.all().filter(
            Q(specialist=context['specialist']),
        )
        if specialist_steam_profile_info:
            context['specialist_steam_profile_info'] = specialist_steam_profile_info[0]
            context['specialist_steam_profile_info_fields'] = {}

            for field in context['specialist_steam_profile_info']._meta.get_fields():
                key = str(field).split('.')[-1]
                if key in ('steamreposinfo>', 'id', 'specialist'):
                    continue

                value = context['specialist_steam_profile_info'][key]
                if value is None:
                    continue

                context['specialist_steam_profile_info_fields'][field.verbose_name] = value

            specialist_steam_repos_objects = SteamReposInfo.objects.all().filter(
                Q(profile=context['specialist_steam_profile_info']),
            )
            specialist_steam_repos_info_fields = []

            for specialist_github_repo_info in specialist_steam_repos_objects:
                specialist_steam_repo_info_fields = {}

                for field in specialist_github_repo_info._meta.get_fields():
                    key = str(field).split('.')[-1]
                    if key in ('id', 'profile'):
                        continue

                    value = specialist_github_repo_info[key]
                    if value is None:
                        value = 0

                    specialist_steam_repo_info_fields[field.verbose_name] = value

                specialist_steam_repos_info_fields.append(specialist_steam_repo_info_fields)

            context['specialist_steam_repos_info_fields'] = specialist_steam_repos_info_fields

        specialist_habr_profile_info = HabrProfileInfo.objects.all().filter(
            Q(specialist=context['specialist']),
        )
        if specialist_habr_profile_info:
            context['specialist_habr_profile_info'] = specialist_habr_profile_info[0]
            context['specialist_habr_profile_info_fields'] = {}

            for field in context['specialist_habr_profile_info']._meta.get_fields():
                key = str(field).split('.')[-1]
                if key in ('habrreposinfo>', 'id', 'specialist'):
                    continue

                value = context['specialist_habr_profile_info'][key]
                if value is None:
                    continue

                context['specialist_habr_profile_info_fields'][field.verbose_name] = value

            specialist_habr_repos_objects = HabrReposInfo.objects.all().filter(
                Q(profile=context['specialist_habr_profile_info']),
            )
            specialist_habr_repos_info_fields = []

            for specialist_github_repo_info in specialist_habr_repos_objects:
                specialist_habr_repo_info_fields = {}

                for field in specialist_github_repo_info._meta.get_fields():
                    key = str(field).split('.')[-1]
                    if key in ('id', 'profile'):
                        continue

                    value = specialist_github_repo_info[key]
                    if value is None:
                        value = 0

                    specialist_habr_repo_info_fields[field.verbose_name] = value

                specialist_habr_repos_info_fields.append(specialist_habr_repo_info_fields)

            context['specialist_habr_repos_info_fields'] = specialist_habr_repos_info_fields

        specialist_stackoverflow_profile_info = StackOverflowProfileInfo.objects.all().filter(
            Q(specialist=context['specialist']),
        )
        if specialist_stackoverflow_profile_info:
            context['specialist_stackoverflow_profile_info'] = specialist_stackoverflow_profile_info[0]
            context['specialist_stackoverflow_profile_info_fields'] = {}

            for field in context['specialist_stackoverflow_profile_info']._meta.get_fields():
                key = str(field).split('.')[-1]
                if key in ('stackoverflowreposinfo>', 'id', 'specialist'):
                    continue

                value = context['specialist_stackoverflow_profile_info'][key]
                if value is None:
                    continue

                context['specialist_stackoverflow_profile_info_fields'][field.verbose_name] = value

        return context


class DetailSpecialistEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'specialists/edit_detail_specialist.html'

    def get_context_data(self, **kwargs):
        context = super(DetailSpecialistEditView, self).get_context_data(**kwargs)
        context['specialist'] = get_object_or_404(
            Specialist,
            pk=kwargs['pk'],
            owner=self.request.user,
        )
        context['specialist_description'] = SpecialistForm(instance=context['specialist'])

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        specialist, specialist_created = Specialist.objects.update_or_create(
            pk=int(self.request.path.split('/')[2]),
            owner=self.request.user,
            defaults={
                'first_name': self.request.POST.get('first_name'),
                'last_name': self.request.POST.get('last_name'),
                'description': self.request.POST.get('description'),
            },
        )

        return redirect(f'/specialists/{specialist.pk}')


class SearchView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def get(self, request):
        data = request.GET.get('data', False).strip().lower().capitalize()

        specialists = Specialist.objects.annotate(
            full_name=Concat('last_name', V(' '), 'first_name')
        ).filter(
            Q(full_name__icontains=data) |
            Q(first_name__icontains=data) |
            Q(last_name__icontains=data)
        )

        if data and specialists:
            return render(
                request,
                'search/search_success.html',
                context={
                    'specialists': specialists,
                    'form': SearchForm(request.GET),
                },
            )
        else:
            return render(
                request,
                'search/search_failure.html',
                context={'form': SearchForm(request.GET)},
            )


class ChoiceInformationSourcesView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def get(self, request):
        return render(
            request,
            'information_sources/choice_information_sources.html',
            context={
                'information_sources': InformationSource.objects.all().order_by('title'),
                'information_sources_selection_form': InformationSourcesSelectionForm,
            },
        )

    def post(self, request, *args, **kwargs):
        form = InformationSourcesSelectionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            information_sources = []

            for source in data:
                if not data[source]:
                    continue
                information_sources.append(source)

            if not information_sources:
                return render(
                    request,
                    'information_sources/choice_information_sources.html',
                    context={
                        'information_sources': InformationSource.objects.all().order_by('title'),
                        'information_sources_selection_form': form,
                    },
                )

            return redirect('application', information_sources=','.join(information_sources))

        return render(
            request,
            'information_sources/choice_information_sources.html',
            context={
                'information_sources': InformationSource.objects.all().order_by('title'),
                'information_sources_selection_form': form,
            },
        )


class ApplicationView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'information_sources/application.html'

    def get_context_data(self, **kwargs):
        information_sources = kwargs['information_sources'].split(',')
        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['forms'] = [InitialDataForm]
        if 'vk' in information_sources:
            context['forms'].append(InitialDataVKForm)
        if 'phone_number_information' in information_sources:
            context['forms'].append(InitialDataPhoneNumberInfoForm)
        if 'github' in information_sources:
            context['forms'].append(InitialDataGitHubForm)
        if 'steam' in information_sources:
            context['forms'].append(InitialDataSteamForm)
        if 'habr' in information_sources:
            context['forms'].append(InitialDataHabrForm)
        if 'stackoverflow' in information_sources:
            context['forms'].append(InitialDataStackOverflowForm)

        return context

    def post(self, request, *args, **kwargs):
        specialist, specialist_created = Specialist.objects.update_or_create(
            first_name=self.request.POST.get('first_name'),
            last_name=self.request.POST.get('last_name'),
            owner=self.request.user,
        )
        information_sources = self.request.path.split('/')[2].split(',')

        if 'vk' in information_sources:
            vk_id = self.request.POST.get('user_id_vk')
            vk_info = VK(vk_id).get_vk_info(self.request.POST.get('visualization_friends', False))

            try:
                vk_data_specialist = VKInfo.objects.get(specialist=specialist, vk_id=vk_info['vk_id'])

                for key, value in vk_info.items():
                    if key == 'vk_id':
                        continue
                    setattr(vk_data_specialist, key, value)

                vk_data_specialist.save()
            except VKInfo.DoesNotExist:
                vk_data_specialist = VKInfo()
                vk_data_specialist.specialist = specialist

                for key, value in vk_info.items():
                    setattr(vk_data_specialist, key, value)

                vk_data_specialist.save()

        if 'phone_number_information' in information_sources:
            info_from_phone_number = PhoneNumber()
            info_from_phone_number(
                self.request.POST.get('phone'),
                specialist,
            )

        if 'github' in information_sources:
            info_from_github = GitHub()
            info_from_github(
                self.request.POST.get('github_nickname'),
                specialist,
            )

        if 'steam' in information_sources:
            info_from_steam = Steam()
            info_from_steam(
                self.request.POST.get('steam_nickname'),
                specialist,
            )

        if 'habr' in information_sources:
            info_from_habr = Habr()
            info_from_habr(
                self.request.POST.get('habr_nickname'),
                specialist,
            )

        if 'stackoverflow' in information_sources:
            info_from_stackoverflow = StackOverflow()
            info_from_stackoverflow(
                self.request.POST.get('stackoverflow_nickname'),
                specialist,
            )

        return redirect(f'/specialists/{specialist.pk}')


class ErrorView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'information_sources/error.html'

    def get_context_data(self, **kwargs):
        type_of_error = kwargs['type_of_error']
        context = super(ErrorView, self).get_context_data(**kwargs)

        if type_of_error == 'BadUserID':
            context['error_text'] = 'Пользователь с таким ID в VK не найден.'
        elif type_of_error == 'ProfileIsPrivate':
            context['error_text'] = 'Профиль пользователя в VK закрыт, в связи с ' \
                                    'чем доступ к некоторому функционалу ограничен.'
        elif type_of_error == 'UserDeletedOrBanned':
            context['error_text'] = 'Профиль пользователя в VK удален или забанен, в ' \
                                    'связи с чем доступ к некоторому функционалу ограничен.'
        elif type_of_error == 'PhoneError':
            context['error_text'] = 'Информация по данному телефону не получена. ' \
                                    'Проверьте введенные данные или повторите попытку позже.'
        elif type_of_error in ('SteamError', 'HabrError'):
            context['error_text'] = 'Информация по данному нику не получена. ' \
                                    'Проверьте введенные данные или повторите попытку позже.'
        elif type_of_error == 'APIRateLimitExceeded':
            context['error_text'] = 'Информация по аккаунту не получена. ' \
                                    'Повторите попытку позже.'
        else:
            context['error_text'] = 'Неопознанная ошибка. Проверьте введенные данные.'

        return context


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


def server_error(request):
    return HttpResponse(request, '<h1>Ой, что-то сломалось</h1>')
