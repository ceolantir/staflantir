from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View
from .models import InformationSource, Specialist
from .forms import InformationSourceForm, SpecialistForm, SearchForm
from django.http import HttpResponseNotFound, HttpResponse


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
        data = request.GET.get('data', False)
        if data:
            specialists = Specialist.objects \
                .filter(Q(first_name__icontains=data) | Q(last_name__icontains=data)) \
                .order_by('last_name')
        else:
            specialists = Specialist.objects.all()
        context = {
            'specialists': specialists,
            'form': SearchForm(request.GET),
        }
        return render(request, 'main/search.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


def server_error(request):
    return HttpResponse(request, '<h1>Ой, что-то сломалось</h1>')
