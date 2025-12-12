# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('samples/', views.SampleListView.as_view(), name='sample-list'),
    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('ethnicities/', views.EthnicityListView.as_view(), name='ethnicity-list'),
    path('tribes/', views.TribeListView.as_view(), name='tribe-list'),
    path('clans/', views.ClanListView.as_view(), name='clan-list'),
    path('haplogroup/', views.HaplogroupCountView.as_view(), name='haplogroup-count'),
    path('haplogroup/all/', views.HaplogroupListView.as_view(), name='haplogroup-list'),
    path('haplogroup/heatmap/', views.HaplogroupHeatmapView.as_view(), name='haplogroup-heatmap'),
]