from rest_framework import generics
from django.db.models import Prefetch
from .models import GeneticSample, Country, Province, City
from .serializers import (
    GeneticSampleSerializer, 
    CountrySerializer, 
    ProvinceSerializer, 
    CitySerializer
)


class SampleListView(generics.ListAPIView):
    serializer_class = GeneticSampleSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = GeneticSample.objects.select_related(
            'province__country',
            'y_dna',
            'mt_dna',
            'historical_period'
        ).all()
        
        country = self.request.query_params.get('country')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')
        
        # Cascade filtering: city > province > country
        if city:
            queryset = queryset.filter(city__name=city)
        elif province:
            queryset = queryset.filter(province__name=province)
        elif country:
            queryset = queryset.filter(province__country__name=country)
            
        return queryset


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    pagination_class = None


class ProvinceListView(generics.ListAPIView):
    serializer_class = ProvinceSerializer
    pagination_class = None
    
    def get_queryset(self):
        queryset = Province.objects.select_related('country').all()
        
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country__name=country)
            
        return queryset.order_by('name')


class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    pagination_class = None
    
    def get_queryset(self):
        queryset = City.objects.select_related('province__country').all()
        
        province = self.request.query_params.get('province')
        if province:
            queryset = queryset.filter(province__name=province)
            
        return queryset.order_by('name')