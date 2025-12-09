from rest_framework import generics
from django.db.models import Prefetch, Q
from .models import GeneticSample, Country, Province, City, Ethnicity, Tribe, Clan
from .serializers import (
    GeneticSampleSerializer, 
    CountrySerializer, 
    ProvinceSerializer, 
    CitySerializer,
    EthnicitySerializer,
    TribeSerializer, # Added
    ClanSerializer # Added
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
            'tribe', # Added
            'clan', # Added
            'y_dna',
            'mt_dna',
            'historical_period'
        ).all()
        
        country = self.request.query_params.get('country')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')
        ethnicity = self.request.query_params.get('ethnicity')
        tribe = self.request.query_params.get('tribe') # Added
        clan = self.request.query_params.get('clan') # Added

        # Cascade filtering: city > province > country
        if city:
            queryset = queryset.filter(city__name=city)
        elif province:
            queryset = queryset.filter(province__name=province)
        elif country:
            queryset = queryset.filter(country__name=country)

        # Hierarchical filtering: clan > tribe
        if clan:
            queryset = queryset.filter(clan__name=clan)
        elif tribe:
            queryset = queryset.filter(tribe__name=tribe)
        
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


class TribeListView(generics.ListAPIView):
    serializer_class = TribeSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Tribe.objects.select_related('ethnicity').all()
        
        ethnicity = self.request.query_params.get('ethnicity')
        if ethnicity:
            queryset = queryset.filter(ethnicity__name=ethnicity)
            
        return queryset.order_by('name')


class ClanListView(generics.ListAPIView):
    serializer_class = ClanSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Clan.objects.select_related('tribe__ethnicity').all()
        
        tribe = self.request.query_params.get('tribe')
        if tribe:
            queryset = queryset.filter(tribe__name=tribe)
        else:
            ethnicity = self.request.query_params.get('ethnicity')
            if ethnicity:
                queryset = queryset.filter(tribe__ethnicity__name=ethnicity)
            
        return queryset.order_by('name')
