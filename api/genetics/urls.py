# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('samples/', views.SampleListView.as_view(), name='sample-list'),
    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('ethnicities/', views.EthnicityListView.as_view(), name='ethnicity-list'),
]