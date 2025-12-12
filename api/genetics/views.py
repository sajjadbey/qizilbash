from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch, Q, Sum
from .models import GeneticSample, Country, Province, City, Ethnicity, Tribe, Clan, YDNATree
from .serializers import (
    GeneticSampleSerializer, 
    CountrySerializer, 
    ProvinceSerializer, 
    CitySerializer,
    EthnicitySerializer,
    TribeSerializer,
    ClanSerializer,
    YDNATreeSerializer,
    HaplogroupCountSerializer
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


class HaplogroupCountView(APIView):
    """
    Returns the total count of samples for a haplogroup including all its subclades.
    Usage: /haplogroup?name=R
    """
    def get(self, request):
        haplogroup_name = request.query_params.get('name')
        
        if not haplogroup_name:
            return Response({'error': 'name parameter is required'}, status=400)
        
        try:
            haplogroup = YDNATree.objects.get(name=haplogroup_name)
        except YDNATree.DoesNotExist:
            return Response({'error': f'Haplogroup {haplogroup_name} not found'}, status=404)
        
        # Get all descendant haplogroups
        def get_all_descendants(node):
            descendants = [node]
            for child in node.children.all():
                descendants.extend(get_all_descendants(child))
            return descendants
        
        all_haplogroups = get_all_descendants(haplogroup)
        haplogroup_ids = [h.id for h in all_haplogroups]
        subclade_names = [h.name for h in all_haplogroups if h.id != haplogroup.id]
        
        # Get total count from all samples (including subclades) using the count field
        all_samples = GeneticSample.objects.filter(y_dna__id__in=haplogroup_ids)
        total_count = all_samples.aggregate(total=Sum('count'))['total'] or 0
        
        # Count samples with this haplogroup directly
        direct_samples = GeneticSample.objects.filter(y_dna=haplogroup)
        direct_count = direct_samples.aggregate(total=Sum('count'))['total'] or 0
        
        # Subclade count is the number of unique subclades (not sample count)
        subclade_count = len(subclade_names)
        
        data = {
            'haplogroup': haplogroup_name,
            'total_count': total_count,
            'direct_count': direct_count,
            'subclade_count': subclade_count,
            'subclades': subclade_names
        }
        
        serializer = HaplogroupCountSerializer(data)
        return Response(serializer.data)


class HaplogroupListView(generics.ListAPIView):
    """
    Lists all haplogroups in hierarchical structure.
    Usage: /haplogroup/all
    """
    serializer_class = YDNATreeSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only root haplogroups (those without parents)
        return YDNATree.objects.filter(parent__isnull=True).order_by('name')
