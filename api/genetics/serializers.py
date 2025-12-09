# serializers.py
from rest_framework import serializers
from .models import GeneticSample, HistoricalPeriod, Country, Province, City, Ethnicity, Tribe, Clan


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class ProvinceSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name')
    
    class Meta:
        model = Province
        fields = ['name', 'country']


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


class GeneticSampleSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', allow_null=True)
    province = serializers.CharField(source='province.name', allow_null=True)
    city = serializers.CharField(source='city.name', allow_null=True)
    ethnicity = serializers.CharField(source='ethnicity.name', allow_null=True)

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
        )

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