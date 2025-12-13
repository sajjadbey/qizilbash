# serializers.py
from rest_framework import serializers
from .models import GeneticSample, HistoricalPeriod, Country, Province, City, Ethnicity, Tribe, Clan, YDNATree


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class ProvinceSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name')
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Province
        fields = ['name', 'country', 'latitude', 'longitude', 'geometry']
    
    def get_latitude(self, obj):
        """Extract latitude from geometry centroid"""
        if obj.geom:
            centroid = obj.geom.centroid
            return float(centroid.y)
        return None
    
    def get_longitude(self, obj):
        """Extract longitude from geometry centroid"""
        if obj.geom:
            centroid = obj.geom.centroid
            return float(centroid.x)
        return None
    
    def get_geometry(self, obj):
        """Return GeoJSON geometry"""
        if obj.geom:
            import json
            return json.loads(obj.geom.geojson)
        return None


class CitySerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province.name')
    
    class Meta:
        model = City
        fields = ['name', 'province']


class EthnicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ethnicity
        fields = ['name']
        
class TribeSerializer(serializers.ModelSerializer):
    ethnicity = serializers.SerializerMethodField()

    class Meta:
        model = Tribe
        fields = ['name', 'ethnicity', 'historical_note']
    def get_ethnicity(self, obj):
        """Returns the ethnicity name, or None/empty string if not set."""
        if obj.ethnicity:
            return obj.ethnicity.name
        return None 


class ClanSerializer(serializers.ModelSerializer):
    tribe = serializers.CharField(source='tribe.name')
    ethnicity = serializers.CharField(source='tribe.ethnicity.name', read_only=True)

    class Meta:
        model = Clan
        fields = ['name', 'tribe', 'ethnicity', 'common_ancestor']


class HistoricalPeriodSerializer(serializers.ModelSerializer):
    display = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = HistoricalPeriod
        fields = ('name', 'start_year', 'end_year', 'display')


class YDNATreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    root_haplogroup = serializers.SerializerMethodField()
    
    class Meta:
        model = YDNATree
        fields = ['name', 'root_haplogroup', 'children']
    
    def get_children(self, obj):
        children = obj.children.all()
        return YDNATreeSerializer(children, many=True).data if children.exists() else []
    
    def get_root_haplogroup(self, obj):
        # Don't include root_haplogroup if this is already a root haplogroup
        if obj.parent is None:
            return None
        return obj.get_root_haplogroup()


class HaplogroupCountSerializer(serializers.Serializer):
    haplogroup = serializers.CharField()
    total_count = serializers.IntegerField()
    direct_count = serializers.IntegerField()
    subclade_count = serializers.IntegerField()
    subclades = serializers.ListField(child=serializers.CharField())


class HaplogroupHeatmapSerializer(serializers.Serializer):
    """Serializer for heatmap data with GeoJSON geometry and sample counts"""
    province = serializers.CharField()
    country = serializers.CharField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    geometry = serializers.JSONField()
    sample_count = serializers.IntegerField()
    haplogroup = serializers.CharField(required=False, allow_null=True)


class GeneticSampleSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', allow_null=True)
    province = serializers.CharField(source='province.name', allow_null=True)
    city = serializers.CharField(source='city.name', allow_null=True)
    ethnicity = serializers.CharField(source='ethnicity.name', allow_null=True)
    coordinates = serializers.SerializerMethodField()

    y_dna = serializers.SerializerMethodField()
    mt_dna = serializers.SerializerMethodField()
    historical_period = HistoricalPeriodSerializer()

    class Meta:
        model = GeneticSample
        fields = (
            'name',
            'country',
            'province',
            'city',
            'ethnicity',
            'tribe',
            'clan',
            'y_dna',
            'mt_dna',
            'historical_period',
            'description',
            'count',
            'coordinates',
        )
    
    def get_coordinates(self, obj):
        """Return coordinates from province geometry centroid if available"""
        if obj.province and obj.province.geom:
            centroid = obj.province.geom.centroid
            return {
                'latitude': float(centroid.y),
                'longitude': float(centroid.x)
            }
        return None

    def get_y_dna(self, obj):
        if obj.y_dna:
            return {
                'name': obj.y_dna.name,
                'root_haplogroup': obj.y_dna.get_root_haplogroup(),
            }
        return None

    def get_mt_dna(self, obj):
        if obj.mt_dna:
            return {
                'name': obj.mt_dna.name,
                'root_haplogroup': obj.mt_dna.get_root_haplogroup(),
            }
        return None