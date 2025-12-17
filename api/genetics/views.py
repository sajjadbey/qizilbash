from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch, Q, Sum, F
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
import json
from .models import (
    GeneticSample, Country, Province, City, Ethnicity, Tribe, Clan, 
    YDNATree, BlogPost
)
from .serializers import (
    GeneticSampleSerializer, 
    CountrySerializer, 
    ProvinceSerializer, 
    CitySerializer,
    EthnicitySerializer,
    TribeSerializer,
    ClanSerializer,
    YDNATreeSerializer,
    HaplogroupCountSerializer,
    HaplogroupHeatmapSerializer,
    BlogPostSerializer
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
        queryset = Tribe.objects.prefetch_related('ethnicities').all()
        
        ethnicity = self.request.query_params.get('ethnicity')
        if ethnicity:
            queryset = queryset.filter(ethnicities__name=ethnicity).distinct()
            
        return queryset.order_by('name')


class ClanListView(generics.ListAPIView):
    serializer_class = ClanSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Clan.objects.select_related('tribe').prefetch_related('tribe__ethnicities').all()
        
        tribe = self.request.query_params.get('tribe')
        if tribe:
            queryset = queryset.filter(tribe__name=tribe)
        else:
            ethnicity = self.request.query_params.get('ethnicity')
            if ethnicity:
                queryset = queryset.filter(tribe__ethnicities__name=ethnicity).distinct()
            
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


class HaplogroupHeatmapView(APIView):
    """
    Returns aggregated sample counts by location with coordinates for heatmap visualization.
    
    Query parameters:
    - haplogroup: Filter by specific Y-DNA haplogroup (optional)
    - country: Filter by country (optional)
    - ethnicity: Filter by ethnicity (optional)
    
    Usage: 
    - /haplogroup/heatmap/ (all samples)
    - /haplogroup/heatmap/?haplogroup=R (samples with R haplogroup and subclades)
    - /haplogroup/heatmap/?country=Iran (samples from Iran)
    """
    def get(self, request):
        haplogroup_name = request.query_params.get('haplogroup')
        country = request.query_params.get('country')
        ethnicity = request.query_params.get('ethnicity')
        
        # Start with all samples
        queryset = GeneticSample.objects.select_related(
            'province__country',
            'y_dna',
            'country',
            'ethnicity'
        ).filter(
            province__isnull=False,
            province__geom__isnull=False
        )
        
        # Filter by haplogroup (including subclades)
        if haplogroup_name:
            try:
                haplogroup = YDNATree.objects.get(name=haplogroup_name)
                
                # Get all descendant haplogroups
                def get_all_descendants(node):
                    descendants = [node]
                    for child in node.children.all():
                        descendants.extend(get_all_descendants(child))
                    return descendants
                
                all_haplogroups = get_all_descendants(haplogroup)
                haplogroup_ids = [h.id for h in all_haplogroups]
                queryset = queryset.filter(y_dna__id__in=haplogroup_ids)
            except YDNATree.DoesNotExist:
                return Response({'error': f'Haplogroup {haplogroup_name} not found'}, status=404)
        
        # Filter by country
        if country:
            queryset = queryset.filter(country__name=country)
        
        # Filter by ethnicity
        if ethnicity:
            queryset = queryset.filter(ethnicity__name=ethnicity)
        
        # Aggregate by province
        from django.db.models import Sum
        from collections import defaultdict
        
        location_data = defaultdict(lambda: {'count': 0, 'province': None, 'country': None, 'lat': None, 'lng': None})
        
        for sample in queryset:
            key = (sample.province.id, sample.province.name)
            location_data[key]['count'] += sample.count
            location_data[key]['province'] = sample.province.name
            location_data[key]['country'] = sample.province.country.name
            # Extract coordinates from geometry centroid and store geometry
            if sample.province.geom:
                centroid = sample.province.geom.centroid
                location_data[key]['lat'] = float(centroid.y)
                location_data[key]['lng'] = float(centroid.x)
                # Store geometry as GeoJSON
                location_data[key]['geometry'] = json.loads(sample.province.geom.geojson)
        
        # Format data for response
        heatmap_data = []
        for (province_id, province_name), data in location_data.items():
            heatmap_data.append({
                'province': data['province'],
                'country': data['country'],
                'latitude': data['lat'],
                'longitude': data['lng'],
                'geometry': data.get('geometry'),
                'sample_count': data['count'],
                'haplogroup': haplogroup_name if haplogroup_name else None
            })
        
        # Sort by sample count descending
        heatmap_data.sort(key=lambda x: x['sample_count'], reverse=True)
        
        serializer = HaplogroupHeatmapSerializer(heatmap_data, many=True)
        return Response(serializer.data)


# Blog Views
class BlogPostListView(generics.ListAPIView):
    """
    List all published blog posts.
    Query parameters:
    - tag: Filter by tag
    - search: Search in title and content
    """
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        # Only show published posts
        queryset = BlogPost.objects.filter(status='published')
        
        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        # Search in title and content
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset.order_by('-published_at', '-created_at')


class BlogPostDetailView(generics.RetrieveAPIView):
    """
    Get a single blog post by slug and increment view count.
    """
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        BlogPost.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        # Refresh instance to get updated view_count
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
