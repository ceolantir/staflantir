from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value as V, Q
from django.db.models.functions import Concat
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View

from . import constants
from .discovery.vk.vk import VK
from .forms import SearchForm, InformationSourcesSelectionForm, InitialDataVKForm, SpecialistForm
from .models import InformationSource, Specialist, VKDataSpecialist


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
        context['specialists'] = Specialist.objects.all().filter(Q(owner=self.request.user)).order_by('last_name')
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
        context['edit'] = False
        context['specialist_data_vk'] = get_object_or_404(
            VKDataSpecialist,
            first_name=context['specialist'].first_name,
            last_name=context['specialist'].last_name,
            specialist=context['specialist'],
        )
        context['specialist_data_vk_fields'] = {}
        for field in context['specialist_data_vk']._meta.get_fields():
            key = str(field).split('.')[-1]
            value = context['specialist_data_vk'][key]

            if not value or key in constants.attribute_exceptions_vk_data_specialist:
                continue
            if key == 'is_closed' and value == 'Закрыт':
                continue

            context['specialist_data_vk_fields'][field.verbose_name] = value

        return context


class DetailSpecialistEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'specialists/detail_specialist.html'

    def get_context_data(self, **kwargs):
        context = super(DetailSpecialistEditView, self).get_context_data(**kwargs)
        context['specialist'] = get_object_or_404(
            Specialist,
            pk=kwargs['pk'],
            owner=self.request.user,
        )
        context['edit'] = True
        context['specialist_description'] = SpecialistForm(instance=context['specialist'])
        context['specialist_data_vk'] = get_object_or_404(
            VKDataSpecialist,
            first_name=context['specialist'].first_name,
            last_name=context['specialist'].last_name,
            specialist=context['specialist'],
        )

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        specialist, specialist_created = Specialist.objects.update_or_create(
            first_name=self.request.POST.get('first_name'),
            last_name=self.request.POST.get('last_name'),
            owner=self.request.user,
            defaults={'description': self.request.POST.get('description')},
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

        if 'vk' in information_sources:
            form = InitialDataVKForm

        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        specialist, specialist_created = Specialist.objects.update_or_create(
            first_name=self.request.POST.get('first_name', 'Нет имени'),
            last_name=self.request.POST.get('last_name', 'Нет фамилии'),
            owner=self.request.user,
        )
        specialist_status = 'Специалист добавлен' if specialist_created else 'Данные специалиста обновлены'

        vk_id = self.request.POST.get('user_id_vk', 'Нет фамилии')
        vk_info = VK(vk_id).get_vk_info(self.request.POST.get('visualization_friends', False))
        try:
            vk_data_specialist = VKDataSpecialist.objects.get(specialist=specialist, vk_id=vk_info['vk_id'])

            for key, value in vk_info.items():
                if key == 'vk_id':
                    continue
                setattr(vk_data_specialist, key, value)

            vk_data_specialist.save()
        except VKDataSpecialist.DoesNotExist:
            vk_data_specialist = VKDataSpecialist()
            vk_data_specialist.specialist = specialist

            for key, value in vk_info.items():
                setattr(vk_data_specialist, key, value)

            vk_data_specialist.save()

        return redirect(f'/specialists/{specialist.pk}')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


def server_error(request):
    return HttpResponse(request, '<h1>Ой, что-то сломалось</h1>')
