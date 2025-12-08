# views.py
from rest_framework import generics
from django.db.models import Prefetch, Q
from .models import GeneticSample, Country, Province, City, Ethnicity
from .serializers import (
    GeneticSampleSerializer, 
    CountrySerializer, 
    ProvinceSerializer, 
    CitySerializer,
    EthnicitySerializer
)


class SampleListView(generics.ListAPIView):
    serializer_class = GeneticSampleSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = GeneticSample.objects.select_related(
            'country',
            'province',
            'city',
            'ethnicity',
            'y_dna',
            'mt_dna',
            'historical_period'
        ).all()
        
        country = self.request.query_params.get('country')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')
        ethnicity = self.request.query_params.get('ethnicity')

        # Cascade filtering: city > province > country, plus separate ethnicity filter
        if city:
            queryset = queryset.filter(city__name=city)
        elif province:
            queryset = queryset.filter(province__name=province)
        elif country:
            queryset = queryset.filter(country__name=country)

        if ethnicity:
            queryset = queryset.filter(ethnicity__name=ethnicity)
            
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


class EthnicityListView(generics.ListAPIView):
    serializer_class = EthnicitySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ethnicity.objects.all().order_by('name')
        
        # Optional: Filter ethnicities based on selected country/province
        # Note: A simple filter based on GeneticSample location is not applied here,
        # but an optional filter based on the M2M field `provinces` is possible.
        # For simplicity, we just return all ethnicities for now, but a more complex
        # query is needed if you want to filter based on samples in the selected location.

        province = self.request.query_params.get('province')
        if province:
            # Filters ethnicities that are linked to the selected province via M2M
            queryset = queryset.filter(provinces__name=province).distinct()
        else:
            country = self.request.query_params.get('country')
            if country:
                # Filters ethnicities that are linked to any province in the selected country
                queryset = queryset.filter(provinces__country__name=country).distinct()

        return queryset.order_by('name')