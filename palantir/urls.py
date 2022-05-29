from django.urls import path

from .views import (
    MainView,
    DetailInformationSourceView,
    SpecialistsView,
    DetailSpecialistView,
    SearchView,
)

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('information_sources/<int:pk>/', DetailInformationSourceView.as_view(), name='detail_information_source'),
    path('specialists/', SpecialistsView.as_view(), name='specialists'),
    path('specialists/<int:pk>/', DetailSpecialistView.as_view(), name='detail_specialist'),
    path('search/', SearchView.as_view(), name='search'),
]
