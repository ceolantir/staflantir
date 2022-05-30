import random
import string

from django.db.models import Value as V, Q
from django.db.models.functions import Concat
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View

from .forms import SearchForm, InformationSourcesSelectionForm
from .models import InformationSource, Specialist


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


class SpecialistsView(TemplateView):
    template_name = 'specialists/all_specialists.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialistsView, self).get_context_data(**kwargs)
        context['specialists'] = Specialist.objects.all().order_by('last_name')
        context['form'] = SearchForm
        return context


class DetailSpecialistView(TemplateView):
    template_name = 'specialists/detail_specialist.html'

    def get_context_data(self, **kwargs):
        context = super(DetailSpecialistView, self).get_context_data(**kwargs)
        context['specialist'] = get_object_or_404(Specialist, pk=kwargs['pk'])
        return context


class SearchView(View):
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


class ChoiceInformationSourcesView(View):
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
                if information_sources is []:
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


class ApplicationView(TemplateView):
    template_name = 'information_sources/application.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['information_sources'] = kwargs['information_sources'].split(',')
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


def server_error(request):
    return HttpResponse(request, '<h1>Ой, что-то сломалось</h1>')
