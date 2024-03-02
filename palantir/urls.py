from django.urls import path

from .views import (
    MainView,
    DetailInformationSourceView,
    SpecialistsView,
    DetailSpecialistView,
    DetailSpecialistEditView,
    SearchView,
    ChoiceInformationSourcesView,
    ApplicationView,
    ErrorView,
)

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('information_sources/<int:pk>/', DetailInformationSourceView.as_view(), name='detail_information_source'),
    path('specialists/', SpecialistsView.as_view(), name='specialists'),
    path('specialists/<int:pk>/', DetailSpecialistView.as_view(), name='detail_specialist'),
    path('specialists/<int:pk>/edit', DetailSpecialistEditView.as_view(), name='detail_specialist_edit'),
    path('search/', SearchView.as_view(), name='search'),
    path('choice_information_sources/', ChoiceInformationSourcesView.as_view(), name='choice_information_sources'),
    path('application/<str:information_sources>/', ApplicationView.as_view(), name='application'),
    path('error/<str:type_of_error>/', ErrorView.as_view(), name='error'),
]
